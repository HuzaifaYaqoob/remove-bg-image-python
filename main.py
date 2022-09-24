
from genericpath import isdir
import tkinter as tk
from tkinter import ttk, filedialog

import cv2

import os


class BackgroundRemover():
    def __init__(self, root_window):
        self.root = root_window
        self.root.title('Background Remover')

        self.root.geometry('700x500+500+300')

        self.selected_images = []
        self.selected_dir = ''

    
    def window_header(self):
        self.header = tk.Frame(self.root)
        self.header.pack(fill=tk.X, padx=10, pady=5)

        heading = tk.Label(self.header, text='Image Background Remover', font=('Roboto', 14))
        heading.pack(pady=5, side=tk.LEFT)

        self.upload_btn = ttk.Button(self.header, text='Select Folder', command=self.UploadBtnClick)
        self.upload_btn.pack(side=tk.RIGHT, padx=4)

        self.process = ttk.Button(self.header, text='Process Images', command=self.FolderProcessing)
        self.process.pack(side=tk.RIGHT,)

    
    def UploadBtnClick(self):
        selected_folder  = filedialog.askdirectory()
        self.selected_dir = selected_folder

    def create_output_folder(self):
        before_location = os.path.abspath(os.getcwd())
        outpt_loc = self.selected_dir.split('/')[0:-1]
        outpt_loc = '/'.join(outpt_loc)
        os.chdir(outpt_loc)
        if not os.path.exists('output'):
            os.mkdir('output')
        os.chdir(before_location)
        

    def imageProcessing(self, file_, save_loc):
        s_img = file_
        image_path = s_img.split('/')
        image_name =  image_path[-1]
        image_name = image_name.split('.')[0:-1]
        image_name = '-'.join(image_name)
        img = cv2.imread(s_img)

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        inverted_img = 255-gray_img


        _ , alpha = cv2.threshold(inverted_img, 0, 255, cv2.THRESH_BINARY )
        # final_image = cv2.divide(gray_img , inverted_img, scale=255.0)
        # if img_ext == 'png':
        # *_, alpha = cv2.split(img)
        final_image = inverted_img
        final_image = cv2.merge((final_image, final_image, final_image, alpha))
        self.create_output_folder()

        before_location = os.path.abspath(os.getcwd())

        if self.selected_dir  == save_loc :
            outpt_loc = self.selected_dir.split('/')[0:-1]
            outpt_loc = '/'.join(outpt_loc)
            os.chdir(outpt_loc)
            cv2.imwrite(f'./output/{image_name}.png', final_image)
            os.chdir(before_location)
        else:
            save_loc = save_loc.split('/')[-1]
            outpt_loc = self.selected_dir.split('/')[0:-1]
            outpt_loc = '/'.join(outpt_loc)
            outpt_loc = outpt_loc + '/output'
            os.chdir(outpt_loc)
            if os.path.exists(save_loc):
                pass
            else:
                os.mkdir(save_loc)

            cv2.imwrite(f'./{save_loc}/{image_name}.png', final_image)
            os.chdir(before_location)


        print('Done')

    def processFoldersRecur(self, folder_name):
        os.chdir(folder_name)
        folder = os.listdir()
        current_folder = os.path.abspath(os.getcwd())

        if len(folder) > 0:
            for i in folder:
                if os.path.isdir(i):
                    self.processFoldersRecur(i)
                    os.chdir(folder_name)
                elif os.path.isfile(i):
                    # print(folder_name)
                    self.imageProcessing(i, current_folder)
                    pass
                else:
                    print('NOT FOUND')
        else:
            print(f'No Directory not found in {folder_name}')


    def FolderProcessing(self):
        self.processFoldersRecur(self.selected_dir)


    def saveImage(self):
        pass



if __name__ == '__main__':
    window = tk.Tk()
    bg_remover = BackgroundRemover(window)
    bg_remover.window_header()
    window.mainloop()