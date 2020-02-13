import torch
import torch.nn as nn
from torchvision import transforms

import time
from PIL import Image
from matplotlib import cm
import matplotlib as mpl
import numpy as np

def double_conv(in_channels, out_channels):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, 3, padding=1),
        nn.ReLU(inplace=True),
        nn.Conv2d(out_channels, out_channels, 3, padding=1),
        nn.ReLU(inplace=True))   


class UNet(nn.Module):

    def __init__(self, n_classes):
        super().__init__()
                
        self.dconv_down1 = double_conv(3, 64)
        self.dconv_down2 = double_conv(64, 128)
        self.dconv_down3 = double_conv(128, 256)
        self.dconv_down4 = double_conv(256, 512)        

        self.maxpool = nn.MaxPool2d(2)
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)        
        
        self.dconv_up3 = double_conv(256 + 512, 256)
        self.dconv_up2 = double_conv(128 + 256, 128)
        self.dconv_up1 = double_conv(128 + 64, 64)
        
        self.conv_last = nn.Conv2d(64, n_classes,1)#,1
        
        
    def forward(self, x):
        conv1 = self.dconv_down1(x)
        x = self.maxpool(conv1)

        conv2 = self.dconv_down2(x)
        x = self.maxpool(conv2)
        
        conv3 = self.dconv_down3(x)
        x = self.maxpool(conv3)   
        
        x = self.dconv_down4(x)
        
        x = self.upsample(x)        
        x = torch.cat([x, conv3], dim=1)
        
        x = self.dconv_up3(x)
        x = self.upsample(x)        
        x = torch.cat([x, conv2], dim=1)       

        x = self.dconv_up2(x)
        x = self.upsample(x)        
        x = torch.cat([x, conv1], dim=1)   
        
        x = self.dconv_up1(x)
        
        out = self.conv_last(x)
        out = torch.sigmoid(out)
        
        return out


class SemanticSegmentation:
    def __init__(self, 
                 model,
                 img_path,
                 img_size, 
                 fp_out):
        """
        model : pretrained unet.
        img_path : path to input image.
        img_size : size for reshape input image.
        fp_out : path to save the output file.
        """

        self.model = model
        self.img_path = img_path
        self.img_size = img_size
        self.fp_out = fp_out

    def get_prediction(self):
        """
        img_path : path to input image.
        preprocess : image preprocessing.
        return semantic segmentation image.
        """
        input_image = Image.open(self.img_path).convert("RGB")
        input_image = input_image.resize((self.img_size, self.img_size))

        preprocess = transforms.Compose([transforms.ToTensor()])

        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            self.model.to('cuda')

        with torch.no_grad():
            print(input_batch.shape)
            output = self.model(input_batch)

        return input_image, output

    def get_segmentation(self):

        """
        input_image : original image.
        output_image :  output from unet.
        return: new image by interpolating between 
        two images,using a constant alpha.
        """
        input_image, output_image = self.get_prediction()

        output_image = output_image.detach().cpu().numpy()[0,0,:,:]
        cm_hot = mpl.cm.get_cmap('cool')
        overlay = cm_hot(output_image)
        overlay = np.uint8(overlay * 255)
        overlay = Image.fromarray(overlay).convert("RGB")

        overlay = overlay.resize((self.img_size, self.img_size))
        input_image = input_image.resize((self.img_size, 
                                         self.img_size))
        heatmap = Image.blend(input_image, overlay, 0.5)

        output_name = str(int(time.time())) + ".png"
        heatmap.save(self.fp_out+output_name, format="PNG")

        return output_name