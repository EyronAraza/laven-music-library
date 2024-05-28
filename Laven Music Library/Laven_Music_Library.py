from tkinter import * 
import customtkinter as CTk 
import tkinter.messagebox as msgBox 
from PIL import ImageTk, Image
import requests
import webbrowser
from io import BytesIO
from urllib.request import urlopen
import random

# Chrome browser file location
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

root = Tk() # make main window

#--- WINDOW CONFIGURATION ---#
root.title("Laven Music Library") # set window's title
root.geometry("700x540") # set window's size
root.config(bg="#DFBBDA") # set background color
root.resizable(0,0) # disable maximize button

#--- CUSTOMISATION ---#
FONT_FAMILY = "Microsoft Sans Serif"
LAVENDER = "#DFBBDA"

#--- FRAMES ---#
#- FRAME 1: Artist Details Page -#
artistDetailsPage = Frame(root)
artistDetailsPage.place(x=0, y=80)
artistDetailsPage.pack_propagate(False)
artistDetailsPage.configure(background="#DFBBDA", height=460, width=700)

#- FRAME 2: Artist Biography Page -#
artistBioPage = Frame(root)

#- FRAME 3: Artist Album Page -#
artistAlbumPage = Frame(root)

#--- API KEY ---#
API_KEY = "523532"

#--- INITIALSATION ---#
artistDetails_Labels = [] # for storing Label widgets of Artist Details
currentTrack = 0 # for navigating the track names using index
currentAlbum = 0 # for navigating the list of albums using index
artist_id = "" # for getting artist id to link it to the API
getLabel_trackName = [] # for storing a label widget of track name
getLabel_artistImage = [] # for storing a label widget of Artist's image

# Function for Searching Artist Name in the Entry widget and then retrieve data from the API
def artistDetailsData(event):
    # Get variables from global space
    global artist_id
    global currentTrack
    global currentAlbum

    currentTrack = 0 # reset current track index 
    currentAlbum = 0 # reset current album index

    searchInput = entry_artist.get() # get input from the entry widget
    searchArtist_name = searchInput.lower() # convert input string to lowercase

    # Access to API link
    searchArtist_req = requests.get(f"https://www.theaudiodb.com/api/v1/json/{API_KEY}/search.php?s={searchArtist_name}")
    artistTrack_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/mvid.php?i={artist_id}")

    # Error Handler: Check if user input nothing or one character
    if searchInput == "" or searchInput == len(searchInput) * searchInput[0]:
        searchCheckError(searchArtist_name)
        return

    # Error Handler: Check if user enters anything other than artist's name
    try:
        # Update Artist's name
        searchArtist_getData = searchArtist_req.json()['artists'][0]['strArtist']
        header_artistName.config(text = searchArtist_getData.upper(), fg="black")

        # Get artist details data from API
        artistDetails_getDataList = [
            searchArtist_req.json()['artists'][0]['strLabel'],
            searchArtist_req.json()['artists'][0]['strGenre'],
            searchArtist_req.json()['artists'][0]['strStyle'],
            searchArtist_req.json()['artists'][0]['intFormedYear'],
            searchArtist_req.json()['artists'][0]['strMood']
            ]

        # Update Artist's Details
        for i in range(len(artistDetails_Labels)):
            # Check if one of the details has a null value or not
            if artistDetails_getDataList[i] is not None:
                artistDetails_Labels[i].config(text = artistDetails_getDataList[i])
            else:
                artistDetails_Labels[i].config(text = "...")

        # Get Artist's ID data from API
        artist_id = searchArtist_req.json()['artists'][0]['idArtist']

        # Update Artist Track's name (for displaying the first track)
        artistTrack_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/mvid.php?i={artist_id}")
        artistTrack_getData = artistTrack_req.json()['mvids'][currentTrack]['strTrack']
        getLabel_trackName[0].config(text = artistTrack_getData)

        # Get Artist's image data from API
        artistImage_getData = searchArtist_req.json()['artists'][0]['strArtistThumb']
        img_url = artistImage_getData
        img_byt = urlopen(img_url)
        img_rawData = img_byt.read()
        img_byt.close()

        # Update Artist's image
        open_pic = Image.open(BytesIO(img_rawData)) # access to image URL's data
        resize_pic = open_pic.resize((200,200), Image.Resampling.LANCZOS) # resize the img
        new_pic = ImageTk.PhotoImage(resize_pic) # use the new img after resize
        getLabel_artistImage[0].config(image=new_pic) # change artist's img
        getLabel_artistImage[0].new_pic = new_pic # updates the img
        
        # Getting the length of the list of artist's tracks
        artistTrack_getData = artistTrack_req.json()['mvids']
        artistTrack_length = len(artistTrack_getData)

        print("[SUCCESS] Artist Found:", searchArtist_getData)
        print("[MESSAGE] Total number of tracks:", artistTrack_length)
    except:
        searchCheckError(searchArtist_name)

# Function for checking an error after entering the search artist bar
def searchCheckError(artistName):
    global artist_id

    print(f"[ERROR] Searching for Artist '{artistName}' not found.")

    # When an error is found, it will reset every data
    header_artistName.config(text = "ARTIST NOT FOUND", fg="red")
    for i in range(len(artistDetails_Labels)):
        artistDetails_Labels[i].config(text = "...")
    getLabel_trackName[0].config(text = "...")
    artist_id=""

    # Reset image
    open_pic = Image.open("Square.png") 
    resize_pic = open_pic.resize((200,200), Image.Resampling.LANCZOS)
    new_pic = ImageTk.PhotoImage(resize_pic) 
    getLabel_artistImage[0].config(image=new_pic) 
    getLabel_artistImage[0].new_pic = new_pic 

# Class for making a container of Artist Details
class artistDetails():
    def __init__(self, master):
        global entry_artist # reference entry widget

        # Border image
        self.open_pic = Image.open("border.png")
        self.resize_border = self.open_pic.resize((665,262), Image.Resampling.LANCZOS) # resize the img
        self.new_pic = ImageTk.PhotoImage(self.resize_border) 
        self.img_border = Label(master, image=self.new_pic, bg=LAVENDER)
        self.img_border.place(anchor="n", relx=0.5, x=0,y=0)

        # Artist image
        self.open_pic2 = Image.open("Square.png") # default image
        self.resize_pic = self.open_pic2.resize((200,200), Image.Resampling.LANCZOS) # resize the img
        self.new_pic2 = ImageTk.PhotoImage(self.resize_pic) # use the new img after resize
        self.img_artist = Label(master, image=self.new_pic2) # create img
        self.img_artist.place(x=100,y=30)
        getLabel_artistImage.append(self.img_artist)

        # Sub-Header "ARTIST'S DETAILS"
        self.header_artistDetails = Label(master, text="ARTIST DETAILS", bg="white", font=(FONT_FAMILY, 20, "bold"))
        self.header_artistDetails.place(anchor="n", relx=0.5, x=110, y=20)

        # List of Artists details
        self.details_list = ["Label:","Genre: ","Style:","Debut Yr:","Mood:"]
        # Place and add spacing between artist details
        place_Y = -5
        space_Y = 35
        # Create Labels of Artists details
        for i in self.details_list:
            place_Y += space_Y
            lbl_details = Label(master, text=i, bg="white", font=(FONT_FAMILY, 15, 'bold'))
            lbl_details.place(x=325, y=place_Y+space_Y)

        # List of data for Artists details
        self.detailsData_list = ["...","...","...","...","..."]
        # Place and add spacing between artist details
        place_Y = -5
        space_Y = 35
        # Create Labels of Artists details data
        for i in self.detailsData_list:
            place_Y += space_Y
            lbl_detailsData = Label(master, text=i, bg="white", font=(FONT_FAMILY, 15))
            lbl_detailsData.place(x=425, y=place_Y+space_Y)
            artistDetails_Labels.append(lbl_detailsData)

        # Text 'Track Name:'
        self.lbl_trackNameTitle = Label(master, text="Track Name:", bg="white", fg="black", font=(FONT_FAMILY, 12,'bold'))
        self.lbl_trackNameTitle.place(anchor="n", relx=0.5, x=0, y=270)

        # Display data of Track Name
        self.lbl_trackName = Label(master, text="...", bg="white", fg="black", font=(FONT_FAMILY, 12))
        self.lbl_trackName.place(anchor="n", relx=0.5, x=0, y=305)
        getLabel_trackName.append(self.lbl_trackName) 

        # List of image file names (for buttons)
        self.imageList = ["previous_button.png", "play_button.png", "next_button.png", "bio_button.png", "random_button.png", "album_button.png"]

        # For storing image files (for buttons)
        self.openImages = []

        # Display first set of buttons
        place_X = -80
        space_X = 80
        for i in range(3):
            self.openImages.append(ImageTk.PhotoImage(Image.open(self.imageList[i]))) # Store image files to the list

            # Create buttons
            self.buttons = Button(master, image=self.openImages[i], bg=LAVENDER, fg=LAVENDER, activebackground = LAVENDER,bd=0, 
                                  command=lambda i=i: onClick(i))
            self.buttons.place(anchor="n", relx=0.5, x=place_X, y=345)

            place_X += space_X # for adding spaces between buttons horizontally 

        # Display second set of buttons
        place_X = -80
        space_X = 80
        for i in range(3,6):
            self.openImages.append(ImageTk.PhotoImage(Image.open(self.imageList[i]))) # Store image files to the list

            # Create buttons
            self.buttons = Button(master, image=self.openImages[i], bg=LAVENDER, fg=LAVENDER, activebackground = LAVENDER,bd=0, 
                                  command=lambda i=i: onClick(i))
            self.buttons.place(anchor="n", relx=0.5, x=place_X, y=400)
            place_X += space_X # for adding spaces between buttons horizontally 

        # Search Artist Bar
        entry_artist = CTk.CTkEntry(master, placeholder_text="Search Artist...", width=145, fg_color="white", text_color="black", font=(FONT_FAMILY, 13))
        entry_artist.place(x=5,y=425)
        entry_artist.bind('<Return>', artistDetailsData)

        # Function for Button commands
        def onClick(btn_index):
            # Get variables from global space
            global currentTrack
            global artist_id

            # Previous button
            if btn_index == 0:
                print("[INPUT] Previous Button")
                navigateTrack(-1) # Go to previous track

            # Play button
            elif btn_index == 1:
                print("[INPUT] Play button")
                openMusicLink()

            # Next  button
            elif btn_index == 2:
                print("[INPUT] Next button")
                navigateTrack(1) # Go to next track

            # Bio button
            elif btn_index == 3:
                print("[INPUT] Bio button")
                biographyPage(master)

            # Shuffle button
            elif btn_index == 4:
                print("[INPUT] Shuffle button")
                shuffleTrack()

            # Album button
            elif btn_index == 5:
                print("[INPUT] Album button")
                albumPage(master)
        
        # Function for opening current track's youtube link
        def openMusicLink():
            # Get variables from global space
            global currentTrack
            global artist_id

            # Access to API link
            artistTrack_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/mvid.php?i={artist_id}")

            # Error Handler if no track is found
            try:
                artistTrack_getData = artistTrack_req.json()['mvids'][currentTrack]['strTrack']
                print(f"[MESSAGE] Opening YouTube MV '{artistTrack_getData}'...")

                # Get Track's youtube video link
                artistTrack_getData = artistTrack_req.json()['mvids'][currentTrack]['strMusicVid']
                webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open_new_tab(artistTrack_getData)
            except:
                print("[ERROR] Track's youtube video not found.")

        # Function for navigating tracks
        def navigateTrack(_trackNo):
            # Get variables from global space
            global currentTrack
            global artist_id

            # Access to API link
            artistTrack_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/mvid.php?i={artist_id}")

            # Error Handler for the purpose of adding boundary
            # (if it reached the track limit, it will go back to the first track)
            try:
                # For manipulating the index thus navigating through tracks
                currentTrack += _trackNo

                # If current track number reaches less than 0, it will go to the last track number (for avoiding negative index)
                if currentTrack < 0:
                     # Getting the length of the list of artist's tracks
                    artistTrack_getData = artistTrack_req.json()['mvids']
                    artistTrack_length = len(artistTrack_getData)
                    currentTrack = artistTrack_length - 1

                # Update Artist Track's name
                artistTrack_getData = artistTrack_req.json()['mvids'][currentTrack]['strTrack']
                self.lbl_trackName.config(text = artistTrack_getData)
                print("[MESSAGE] Track No.:",currentTrack + 1)
            except:
                # Error Handler if track is found or not
                try:
                    # Go back to first track if reached the track limit
                    currentTrack = 0
                    artistTrack_getData = artistTrack_req.json()['mvids'][currentTrack]['strTrack']
                    self.lbl_trackName.config(text = artistTrack_getData)
                    print("[MESSAGE] Track No.:",currentTrack + 1)
                except:
                    print("[ERROR] Track not found.")

        # Function for shuffling track
        def shuffleTrack():
            # Get variables from global space
            global currentTrack
            global artist_id

            # Access to API link
            artistTrack_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/mvid.php?i={artist_id}")

            # Error Handler if no track is found
            try:
                # Getting the length of the list of artist's tracks
                artistTrack_getData = artistTrack_req.json()['mvids']
                artistTrack_length = len(artistTrack_getData)

                # Randomising and then selecting a track number 
                artistTrack_randomiseNum = random.randint(0, artistTrack_length - 1) 
                print(f"[MESSAGE] Randomising a track from a total of '{artistTrack_length}' tracks")
                print("[MESSAGE] Track number selected:", artistTrack_randomiseNum + 1)

                # Update Artist Track's name
                currentTrack = artistTrack_randomiseNum
                artistTrack_getData = artistTrack_req.json()['mvids'][currentTrack]['strTrack']
                self.lbl_trackName.config(text = artistTrack_getData)
            except:
                print("[ERROR] Track not found.")

        # Function for biography page
        def biographyPage(self):
            # Get variables from global space
            global artistBioPage 
            global artist_id

            # Biography frame
            artistBioPage.place(x=0, y=80)
            artistBioPage.pack_propagate(False)
            artistBioPage.configure(background="#DFBBDA", height=460, width=700)

            # Border
            open_pic = Image.open("border.png")
            resize_pic = open_pic.resize((600,390), Image.Resampling.LANCZOS)
            new_pic = ImageTk.PhotoImage(resize_pic) 
            img_border = Label(artistBioPage, image=new_pic, bg=LAVENDER)
            img_border.place(anchor="n", relx=0.5, x=0,y=0)
            img_border.newpic = new_pic

            # Sub-Header 'Biography'
            lbl_biographyText = Label(artistBioPage, text="BIOGRAPHY", fg="black", bg="white", font=(FONT_FAMILY, 15, 'bold'))
            lbl_biographyText.place(anchor="n", relx=0.5, x=0,y=10) 

            # Error Handler if artist is found or not to display their image
            try:
                searchArtist_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/artist.php?i={artist_id}")
                artistImage_getData = searchArtist_req.json()['artists'][0]['strArtistThumb']
                img_url = artistImage_getData
                img_byt = urlopen(img_url)
                img_rawData = img_byt.read()
                img_byt.close()
                self.open_pic2 = Image.open(BytesIO(img_rawData)) # artist image
            except:
                self.open_pic2 = Image.open("Square.png") # default image
                print("[ERROR] Artist not found for Biography page.")

            # Artist image
            self.resize_pic = self.open_pic2.resize((170,170), Image.Resampling.LANCZOS) # resize the img
            self.new_pic2 = ImageTk.PhotoImage(self.resize_pic) # use the new img after resize
            self.img_artist = Label(artistBioPage, image=self.new_pic2) # create img
            self.img_artist.place(anchor="n", relx=0.5, x=0, y=50)

            # Error handler if artist is found or not to display biography info
            try:
                # Get Artist's biography data from API
                artistBio_getData = searchArtist_req.json()['artists'][0]['strBiographyEN']
                bioStringText = artistBio_getData
            except:
                bioStringText = "No biography information."

            # Artist Biography Information (as textbox widget)
            textbox_bioInfo = CTk.CTkTextbox(artistBioPage, height=130, width=530, fg_color="white",
                                             text_color="black", border_color="black", border_width=2, font=(FONT_FAMILY, 14), wrap=WORD)
            textbox_bioInfo.place(anchor="n", relx=0.5, x=0, y=240)
            textbox_bioInfo.insert("0.0", bioStringText)  # insert at line 0 character 0

            # Go Back Button
            btn_goBack = CTk.CTkButton(artistBioPage, text="GO BACK", fg_color="white", text_color="black", corner_radius=5, 
                                       font=(FONT_FAMILY, 15), hover_color="#c4c4c4", command=goBackToMainPage)
            btn_goBack.place(anchor="n", relx=0.5, x=0, y=410)

        def albumPage(self):
            # Get variables from global space
            global artistAlbum
            global artistAlbumPage
            global artist_id
            global currentAlbum

            # Request API
            artistAlbum_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/album.php?i={artist_id}")

            # Biography frame
            artistAlbumPage.place(x=0, y=80)
            artistAlbumPage.pack_propagate(False)
            artistAlbumPage.configure(background="#DFBBDA", height=460, width=700)

            # Border
            open_pic = Image.open("border.png")
            resize_pic = open_pic.resize((600,390), Image.Resampling.LANCZOS)
            new_pic = ImageTk.PhotoImage(resize_pic) 
            img_border = Label(artistAlbumPage, image=new_pic, bg=LAVENDER)
            img_border.place(anchor="n", relx=0.5, x=0,y=0)
            img_border.newpic = new_pic

            # Sub-header 'Album'
            lbl_albumNameSub = Label(artistAlbumPage, text="ALBUM:" , fg="black", bg="white", font=(FONT_FAMILY, 15, 'bold'))
            lbl_albumNameSub.place(anchor="n", relx=0.5, x=0,y=6) 

            # Update Album Name
            try:
                albumName_getData = artistAlbum_req.json()['album'][currentAlbum]['strAlbum']
                lbl_albumName = Label(artistAlbumPage, text=albumName_getData , fg="black", bg="white", font=(FONT_FAMILY, 14))
                lbl_albumName.place(anchor="n", relx=0.5, x=0,y=33) 
            except:
                lbl_albumName = Label(artistAlbumPage, text="..." , fg="black", bg="white", font=(FONT_FAMILY, 14))
                lbl_albumName.place(anchor="n", relx=0.5, x=0,y=33) 

            # Get Artist's Album image data from API
            try:
                artistAlbumImage_getData = artistAlbum_req.json()['album'][currentAlbum]['strAlbumThumb']
                img_url = artistAlbumImage_getData
                img_byt = urlopen(img_url)
                img_rawData = img_byt.read()
                img_byt.close()

                artistAlbum_getData = artistAlbum_req.json()['album']
                artistAlbumTotal = len(artistAlbum_getData)
                print("[MESSAGE] Total albums:", artistAlbumTotal)
            except:
                print("[ERROR] Artist not found for Album page.")

            # Error Handler if artist is found or not to display their album image
            try:
                open_albumPic = Image.open(BytesIO(img_rawData)) # album image
            except:
                open_albumPic = Image.open("Square.png") # default image

            # Artist Album image
            resize_pic = open_albumPic.resize((170,170), Image.Resampling.LANCZOS) # resize the img
            new_pic = ImageTk.PhotoImage(resize_pic) # use the new img after resize
            img_album = Label(artistAlbumPage, image=new_pic) # create img
            img_album.place(anchor="n", relx=0.5, x=0, y=65)
            img_album.new_pic = new_pic

            # Display page number for albums
            try:
                currentPageText = str(currentAlbum + 1)
                maxPageText = str(artistAlbumTotal)
                displayPageText = f"Page {currentPageText} of {maxPageText}"
                lbl_pageNum = Label(artistAlbumPage, text=displayPageText, fg="black", bg="white", font=(FONT_FAMILY, 10, 'bold'))
                lbl_pageNum.place(anchor="n", relx=0.5, x=0,y=238)
            except:
                # If no album found, display no pages
                lbl_pageNum = Label(artistAlbumPage, text="Page 0 of 0", fg="black", bg="white", font=(FONT_FAMILY, 10, 'bold'))
                lbl_pageNum.place(anchor="n", relx=0.5, x=0,y=238)
            
            # Error Handler if artist is found or not to display Album info
            try:
                # Get Artist's album data from API
                albumInfo_getData = artistAlbum_req.json()['album'][currentAlbum]['strDescriptionEN']
                albumInfoText = albumInfo_getData
            except:
                albumInfoText = "No album information."

            # Artist Album Information (as textbox widget)
            textbox_albumInfo = CTk.CTkTextbox(artistAlbumPage, height=115, width=530, fg_color="white",
                                             text_color="black", border_color="black", border_width=2, font=(FONT_FAMILY, 14), wrap=WORD)
            textbox_albumInfo.place(anchor="n", relx=0.5, x=0, y=264)
            textbox_albumInfo.insert("0.0", albumInfoText)  # insert at line 0 character 0

            # Previous Button
            btn_prevAlbum = CTk.CTkButton(artistAlbumPage, text="<<", width=20, height=10, fg_color="white", text_color="black", corner_radius=5,
                                          font=(FONT_FAMILY, 14), hover_color="#c4c4c4", command=lambda: navigateAlbum(-1, img_album, lbl_albumName, lbl_pageNum, textbox_albumInfo))
            btn_prevAlbum.place(anchor="n", relx=0.5, x=-105, y=413)

            # Next Button
            btn_nextAlbum = CTk.CTkButton(artistAlbumPage, text=">>", width=20, height=10, fg_color="white", text_color="black", corner_radius=5,
                                          font=(FONT_FAMILY, 14), hover_color="#c4c4c4", command=lambda: navigateAlbum(1, img_album, lbl_albumName, lbl_pageNum, textbox_albumInfo))
            btn_nextAlbum.place(anchor="n", relx=0.5, x=105, y=413)

            # Go Back Button
            btn_goBack = CTk.CTkButton(artistAlbumPage, text="GO BACK", fg_color="white", text_color="black", corner_radius=5, 
                                       font=(FONT_FAMILY, 15), hover_color="#c4c4c4", command=goBackToMainPage)
            btn_goBack.place(anchor="n", relx=0.5, x=0, y=410)

        def navigateAlbum(_albumNum, _albumImg, _albumName, _pageNum, _textbox):
            # Get variables from global space
            global currentAlbum
            global artist_id

            # Access to API link
            artistAlbum_req = requests.get(f"https://theaudiodb.com/api/v1/json/2/album.php?i={artist_id}")

            # Error Handler if album is found or not
            try:
                # Album navigation using index
                currentAlbum += _albumNum

                # Implement page boundaries
                artistAlbum_getData = artistAlbum_req.json()['album']
                artistAlbumTotal = len(artistAlbum_getData)
                if (currentAlbum >= artistAlbumTotal):
                    currentAlbum = 0
                elif (currentAlbum < 0):
                    currentAlbum = artistAlbumTotal - 1

                print("[MESSAGE] Album Page:", currentAlbum + 1)

                # Update Album Name
                albumName_getData = artistAlbum_req.json()['album'][currentAlbum]['strAlbum']
                _albumName.config(text=albumName_getData)

                # Get Artist's Album image data from API
                try:
                    artistAlbumImage_getData = artistAlbum_req.json()['album'][currentAlbum]['strAlbumThumb']
                    img_url = artistAlbumImage_getData
                    img_byt = urlopen(img_url)
                    img_rawData = img_byt.read()
                    img_byt.close()
                except:
                    print("[ERROR] Artist not found for Album page.")

                 # Error Handler if artist is found or not to display their album image
                try:
                    open_albumPic = Image.open(BytesIO(img_rawData)) # album image
                except:
                    open_albumPic = Image.open("Square.png") # default image

                # Update Artist Album image
                resize_pic = open_albumPic.resize((170,170), Image.Resampling.LANCZOS) # resize the img
                new_pic = ImageTk.PhotoImage(resize_pic) # use the new img after resize
                _albumImg.config(image=new_pic)
                _albumImg.new_pic = new_pic

                # Error Handler if artist is found or not to display Album info
                try:
                    # Get Artist's album data from API
                    albumInfo_getData = artistAlbum_req.json()['album'][currentAlbum]['strDescriptionEN']
                    albumInfoText = albumInfo_getData

                    # Check if the Album info is null
                    if albumInfoText is None:
                        albumInfoText = "No album information."
                except:
                    albumInfoText = "No album information."

                # Update Album info
                _textbox.delete("0.0", "end")
                _textbox.insert("0.0", albumInfoText)

                # Display page number for albums
                currentPageText = str(currentAlbum + 1)
                maxPageText = str(artistAlbumTotal)
                displayPageText = f"Page {currentPageText} of {maxPageText}"
                _pageNum.config(text=displayPageText)
            except:
                print("[ERROR] Album not found.")

        # Function for going back to main page
        def goBackToMainPage():
            artistBioPage.place_forget() # disable biography page
            artistAlbumPage.place_forget() # disable album page
            

# Header "ARTIST'S NAME"
header_artistName = Label(root, text="ARTIST'S NAME", bg="white", fg="black", font=(FONT_FAMILY,40,'bold'))
header_artistName.place(anchor="n", relx=0.5, x=0, y=5)

# Call Artist Details class to display as main page
artistDetails(artistDetailsPage)

#- FRAME 0: Intro Page -#
artistIntroPage = Frame(root)
artistIntroPage.pack_propagate(False)
artistIntroPage.configure(background="#DFBBDA", height=540, width=700)
artistIntroPage.place(x=0, y=0)

group_y=70 # for positioning group of certain widgets

# Introduction Header
header_intro = Label(artistIntroPage, text="Welcome to Laven", bg="white", fg="#896790", font=(FONT_FAMILY,40,'bold'))
header_intro.place(anchor="n", relx=0.5, x=0, y=20+group_y)

# Opening text file to insert it to Introduction Textbox
with open("intro.txt", "r") as file_handler:
    introText = file_handler.read()

# Introduction Textbox
textbox_intro = CTk.CTkTextbox(artistIntroPage, height=150, width=550, fg_color="white",
                                             text_color="black", border_color="black", border_width=2, font=(FONT_FAMILY, 18), wrap=WORD)
textbox_intro.place(anchor="n", relx=0.5, x=0, y=150+group_y)
textbox_intro.insert("0.0", introText)

# Function for 'Get Started' Button to remove the introduction page
def startButton():
    artistIntroPage.destroy()

# Get Started Button
btn_start = CTk.CTkButton(artistIntroPage, text="GET STARTED", fg_color="white", text_color="black", corner_radius=5, 
                            font=(FONT_FAMILY, 15), hover_color="#c4c4c4", command=startButton)
btn_start.place(anchor="n", relx=0.5, x=0, y=340+group_y)

root.mainloop()
