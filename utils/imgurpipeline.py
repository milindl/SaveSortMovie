'''
Imgur pipeline to convert any local images to imgur
Then use the links to do necessary operations
'''
from imgurpython import ImgurClient

class ImgurPipeline:
    '''
    ImgurPipeline is used to pipe any image thru imgur
    '''
    def __init__(self, img_path, client, path_type = 'path'):
        '''
        __init__ usage:
        img path can be a url or an os path
        client is an imgurpython.ImgurClient
        path_type decides if img_path is ospath(default) or url
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
        get_link
        Returns image link if available
        Else throws error
        '''
        if self.useable:
            return self.img['link']
        raise ValueError('IO after deleting image')

    def delete(self):
        '''
        Delete image after use
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
        
