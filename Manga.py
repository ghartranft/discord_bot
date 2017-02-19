class manga:
    def __init__(self, content=None):
        self.content = content
        self.magazine_text = None
        self.store_link = None
        
    def populate_name(self):
        self.content_name = self.content['content_name']

    def populate_url(self):
        self.content_url = self.content['content_url']

    def populate_artists(self, artists, length):
        self.content_artists = list()
        for i in range(0, length):
            self.content_artists.append(artists[i]['attribute'])

    def populate_tags(self, tags, length):
        self.content_tags = list()
        for i in range(0, length):
            self.content_tags.append(tags[i]['attribute'])

    def populate_date(self):
        self.content_date = self.content['content_date']

    def populate(self):
        self.populate_name()
        self.populate_url()
        self.populate_date()
        try:
            self.populate_artists(self.content['content_artists'], len(self.content['content_artists']))
        except KeyError:
            self.content_artists = None
        
        try:
            self.populate_tags(self.content['content_tags'], len(self.content['content_tags']))
        except KeyError:
            self.content_tags = None
        

    def set_store_link(self, link):
        self.store_link = link

    def set_magazine_text(self, text):
        self.magazine_text = text

    def print_all(self):
        print(self.content_name)
        print(self.content_url)
        print(self.content_artists)
        print(self.content_tags)
        print(self.content_date)
