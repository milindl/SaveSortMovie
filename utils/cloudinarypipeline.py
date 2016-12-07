import cloudinary
import cloudinary.uploader
import cloudinary.api

class CloudinaryPipeline:
    '''
    This converts any local image to cloudinary
    Returns the links for further use
    Deletes the images after use
    
    class CloudinaryPipeline:

    Properties: 
    Methods:
    '''

    def __init__(self, img_path,authentication_data, path_type = 'path'):
        '''
        __init__(img_path, path_type = 'path')
        img_path: url/filepath
        path_type: 'url'/'path'
        '''
        cloudinary.config(
            cloud_name = authentication_data['cloud_name'],
            api_key = authentication_data['api_key'],
            api_secret = authentication_data['api_secret']
            )
        self.img = cloudinary.uploader.upload(img_path)
        self.useable = True


    def get_link(self):
        '''
        get_link(): string
        Returns link of image we're piping
        If deleted, raises Error
        '''
        if self.useable:
            return self.img['url']
        raise ValueError('IO After deleting image')

    def delete(self):
        '''
        delete()
        Delete image after use
        '''
        self.useable = False
        cloudinary.uploader.destroy(self.img['public_id'])
        
