"""

Utilities included here for collagen segmentation task.  

This includes:

output figure generation, 
metrics calculation,
etc.


"""

import torch
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

from PIL import Image

from Segmentation_Metrics_Pytorch.metric import BinaryMetrics

def back_to_reality(tar):
    
    # Getting target array into right format
    classes = np.shape(tar)[-1]
    dummy = np.zeros((np.shape(tar)[0],np.shape(tar)[1]))
    for value in range(classes):
        mask = np.where(tar[:,:,value]!=0)
        dummy[mask] = value

    return dummy

def apply_colormap(img):

    #print(f'Size of image: {np.shape(img)}')
    #print(f'Min:{np.min(img)}, Max: {np.max(img)}, Type: {img.dtype}')
    n_classes = np.shape(img)[-1]

    image = img[:,:,0]
    for cl in range(1,n_classes):
        image = np.concatenate((image, img[:,:,cl]),axis = 1)

    return image

 """   
 # This visualization function can be used for binary outputs
def visualize(images,output_type):
    
    n = len(images)
    
    for i,key in enumerate(images):

        plt.subplot(1,n,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.title(key)
        
        if len(np.shape(images[key]))==4:
            img = images[key][0,:,:,:]
        else:
            img = images[key]
            
        img = np.float32(np.moveaxis(img, source = 0, destination = -1))
        #print(key)
        if key == 'Pred_Mask' or key == 'Ground_Truth':
            if output_type=='binary' or key == 'Ground_Truth':
                #print('using back_to_reality')
                img = back_to_reality(img)

                plt.imshow(img)
            if output_type == 'continuous' and not key == 'Ground_Truth':
                #print('applying colormap')
                img = apply_colormap(img)

                plt.imshow(img,cmap='jet')
        else:
            plt.imshow(img)

    return plt.gcf()
    """

def visualize_continuous(images,output_type):

    if output_type=='comparison':
        n = len(images)
        for i,key in enumerate(images):

            plt.subplot(1,n,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.title(key)

            if len(np.shape(images[key])) == 4:
                img = images[key][0,:,:,:]
            else:
                img = images[key]

            img = np.float32(img)

            if np.shape(img)[0]<np.shape(img)[-1]:
                img = np.moveaxis(img,source=0,destination=-1)

            if key == 'Pred_Mask' or key == 'Ground_Truth':
                img = apply_colormap(img)

                plt.imshow(img,cmap='jet')
            else:
                plt.imshow(img)
        output_fig = plt.gcf()

    elif output_type=='prediction':
        pred_mask = images['Pred_Mask']

        if len(np.shape(pred_mask))==4:
            pred_mask = pred_mask[0,:,:,:]

        pred_mask = np.float32(pred_mask)

        if np.shape(pred_mask)[0]<np.shape(pred_mask)[-1]:
            pred_mask = np.moveaxis(img,source=0,destination = -1)

        output_fig = apply_colormap(pred_mask)


    return output_fig


def get_metrics(pred_mask,ground_truth,img_name,calculator,target_type):

    metrics_row = {}

    if target_type=='binary':
        edited_gt = ground_truth[:,1,:,:]
        edited_gt = torch.unsqueeze(edited_gt,dim = 1)
        edited_pred = pred_mask[:,1,:,:]
        edited_pred = torch.unsqueeze(edited_pred,dim = 1)

            #print(f'edited pred_mask shape: {edited_pred.shape}')
            #print(f'edited ground_truth shape: {edited_gt.shape}')
            #print(f'Unique values prediction mask : {torch.unique(edited_pred)}')
            #print(f'Unique values ground truth mask: {torch.unique(edited_gt)}')

        acc, dice, precision, recall,specificity = calculator(edited_gt,torch.round(edited_pred))
        metrics_row['Accuracy'] = [round(acc.numpy().tolist(),4)]
        metrics_row['Dice'] = [round(dice.numpy().tolist(),4)]
        metrics_row['Precision'] = [round(precision.numpy().tolist(),4)]
        metrics_row['Recall'] = [round(recall.numpy().tolist(),4)]
        metrics_row['Specificity'] = [round(specificity.numpy().tolist(),4)]
        
        #print(metrics_row)
    elif target_type == 'nonbinary':
        square_diff = (ground_truth.numpy()-pred_mask.numpy())**2
        mse = np.mean(square_diff)

        metrics_row['MSE'] = [round(mse,4)]

    metrics_row['ImgLabel'] = img_name

    return metrics_row











