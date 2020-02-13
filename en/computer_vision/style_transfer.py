
import numpy as np
import matplotlib as mpl
from matplotlib import cm
import time


import torch
import torch.nn as nn

from PIL import Image

class TransformerNetwork(nn.Module):
    """Feedforward Transformation Network without Tanh
    reference: https://arxiv.org/abs/1603.08155
    exact architecture: https://cs.stanford.edu/people/jcjohns/papers/fast-style/fast-style-supp.pdf
    """
    def __init__(self):
        super(TransformerNetwork, self).__init__()
        self.ConvBlock = nn.Sequential(
            ConvLayer(3, 32, 9, 1),
            nn.ReLU(),
            ConvLayer(32, 64, 3, 2),
            nn.ReLU(),
            ConvLayer(64, 128, 3, 2),
            nn.ReLU()
        )
        self.ResidualBlock = nn.Sequential(
            ResidualLayer(128, 3),
            ResidualLayer(128, 3),
            ResidualLayer(128, 3),
            ResidualLayer(128, 3),
            ResidualLayer(128, 3)
        )
        self.DeconvBlock = nn.Sequential(
            DeconvLayer(128, 64, 3, 2, 1),
            nn.ReLU(),
            DeconvLayer(64, 32, 3, 2, 1),
            nn.ReLU(),
            ConvLayer(32, 3, 9, 1, norm="None")
        )

    def forward(self, x):
        x = self.ConvBlock(x)
        x = self.ResidualBlock(x)
        out = self.DeconvBlock(x)
        return out



class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, norm="instance"):
        super(ConvLayer, self).__init__()
        # Padding Layers
        padding_size = kernel_size // 2
        self.reflection_pad = nn.ReflectionPad2d(padding_size)

        # Convolution Layer
        self.conv_layer = nn.Conv2d(in_channels, out_channels, kernel_size, stride)

        # Normalization Layers
        self.norm_type = norm
        if (norm=="instance"):
            self.norm_layer = nn.InstanceNorm2d(out_channels, affine=True)
        elif (norm=="batch"):
            self.norm_layer = nn.BatchNorm2d(out_channels, affine=True)

    def forward(self, x):
        x = self.reflection_pad(x)
        x = self.conv_layer(x)
        if (self.norm_type=="None"):
            out = x
        else:
            out = self.norm_layer(x)
        return out

class ResidualLayer(nn.Module):
    """
    Deep Residual Learning for Image Recognition
    https://arxiv.org/abs/1512.03385
    """
    def __init__(self, channels=128, kernel_size=3):
        super(ResidualLayer, self).__init__()
        self.conv1 = ConvLayer(channels, channels, kernel_size, stride=1)
        self.relu = nn.ReLU()
        self.conv2 = ConvLayer(channels, channels, kernel_size, stride=1)

    def forward(self, x):
        identity = x                     # preserve residual
        out = self.relu(self.conv1(x))   # 1st conv layer + activation
        out = self.conv2(out)            # 2nd conv layer
        out = out + identity             # add residual
        return out

class DeconvLayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, output_padding, norm="instance"):
        super(DeconvLayer, self).__init__()

        # Transposed Convolution
        padding_size = kernel_size // 2
        self.conv_transpose = nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding_size, output_padding)

        # Normalization Layers
        self.norm_type = norm
        if (norm=="instance"):
            self.norm_layer = nn.InstanceNorm2d(out_channels, affine=True)
        elif (norm=="batch"):
            self.norm_layer = nn.BatchNorm2d(out_channels, affine=True)

    def forward(self, x):
        x = self.conv_transpose(x)
        if (self.norm_type=="None"):
            out = x
        else:
            out = self.norm_layer(x)
        return out










class NeuralStyleTransfer:
    def __init__(self, 
                 model,
                 input_img,
                 img_size,
                 fp_out,
                 device="cpu"):
        """
        model: neural network for style_transfer.
        #style_path : path to predtrain transfer style weights.
        input_img : path to input image.
        img_size : size for resize image, keeping aspect ratio,
        due to computational limitations.
        fp_out : path to save the output file.
        """
        self.model = model
        self.input_img = input_img
        self.img_size = img_size
        self.fp_out = fp_out
        self.device = device

    def resize_img(self, image):
        h = image.size[0]
        w = image.size[1]
        ratio = h *1.0 / w

        if ratio > 1:
            h = self.img_size
            w = int(h*1.0/ratio)
        else:
            w = self.img_size
            h = int(w * ratio)

        img = np.array(image.resize((h, w), Image.BICUBIC))

        return img


    def get_style(self):

        """ ,
        BGR2RGB then Normalization from (0,1).
        return name of output file.
        """

        image = Image.open(self.input_img).convert("RGB")
        image = self.resize_img(image)

        image = np.array(image).transpose(2, 1, 0)
        image_tensor = torch.tensor(image).float().unsqueeze(0)

        content_batch = image_tensor[:, [2, 1, 0]].to(self.device)
        output =  self.model(content_batch)

        output_image = output[0, :, :, :].detach().cpu().numpy().transpose(2, 1, 0)
        output_image = np.array(output_image / 255).clip(0, 1)
        output_image = Image.fromarray((output_image[...,[2,1,0]] * 255).astype(np.uint8))

        output_name = str(int(time.time())) + ".png"
        output_image.save(self.fp_out+output_name, format="PNG")

        return output_name
