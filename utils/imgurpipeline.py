
'''
imgurpipeline.py
class ImgurPipeline
test methods
'''
from imgurpython import ImgurClient


class ImgurPipeline:
    '''
    Imgur pipeline to convert any local images to imgur
    Then use the links to do necessary operations.
    Delete the image after use
    class ImgurPipeline:

    Properties: 
    - client : ImgurClient used to communicate with imgur
    - img : JSON containing output of upload() of client
    - useable : boolean deciding whether img is still useable

    Methods: 
    __init__(img_path, client, path_type)
    get_link()
    delete()

    '''

    def __init__(self, img_path, client, path_type = 'path'):
        '''
        __init__(img_path, client, path_type = 'path')
        img_path : URL or filepath to image
        client : pre-made ImgurClient
        path_type : 'url' or 'path' depending on img_path

        '''
        self.client = client
        self.img = None
        if path_type == 'url':
            self.img = client.upload_from_url(
                img_path,
                anon=True,
                config=None
            )
        else:
            self.img = client.upload_from_path(
                img_path,
                anon=True,
                config=None
            )
        self.useable = True
        
    def get_link(self):
        '''
        get_link() : string 
        Returns link of image we are piping
        If image is deleted, raises ValueError
        '''
        if self.useable:
            return self.img['link']
        raise ValueError('IO after deleting image')

    def delete(self):
        '''
        delete()
        Delete image after use.
        '''
        self.client.delete_image(self.img['deletehash'])
        self.useable = False
        
if __name__=='__main__':
    # Testing
    c_id = ''
    c_secret = ''
    with open("CLIENT_DATA", "r") as cfile:
        lines = cfile.readlines()
        c_id = lines[0].split(':')[1][:-1]
        c_secret = lines[1].split(':')[1][:-1]
    i_client = ImgurClient(c_id, c_secret)
    ip = ImgurPipeline('/home/path/path/path', i_client)
    print(ip.get_link())
    a = raw_input('Delete image?')
    ip.delete()
        
