"""📄 Image Extractor and PDF Converter

This script scrapes images (JPG, PNG, WEBP) from a given webpage URL using BeautifulSoup and Requests.
It displays the images in a Tkinter GUI with checkboxes for selection. Selected images are converted
and saved as a single PDF file.

Features:
- Supports JPG, PNG, and WEBP formats
- Scrolling preview with checkboxes
- Toggle all selections
- Rename output PDF
- Simple PDF export

Usage:
1. Run the script.
2. Enter the URL of the webpage with images.
3. Preview and select images from the GUI.
4. Save the selected images as a PDF.

Note:
This is not a PDF editor. For reordering pages or more advanced editing, use a dedicated PDF tool.
"""


from bs4 import BeautifulSoup
from requests import get
from urllib.parse import urljoin
from PIL.Image import open, Resampling
from PIL.ImageTk import PhotoImage
from io import BytesIO
from re import sub
from tqdm import tqdm
from ttkbootstrap import Window, Checkbutton, BooleanVar, Frame, Button
from ttkbootstrap.scrolled import ScrolledFrame
from sys import exit


def extract_images_as_pil(url: str, files: list[str] | str = ['jpg', 'png', 'webp']):
    """This function creates list of PIL.Image objects and title of the webpage.\n
example:\n
list_of_image, title = extract_images_as_pil(url = 'https://www.examplesite.com', files = ['jpg', 'webp'])\n
list_of_image[0].show()\n
print(str(title))\n"""
    
    try:
        response = get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title else "Untitled"
    pictures = soup.find_all("img")
    print(f"Found {len(pictures)} images. Downloading...")

    pil_images = []

    for idx, picture in enumerate(tqdm(pictures, desc="Downloading images"), start=1):
        image_url = None
        
        if picture:
            image_url = picture.get("data-src") or picture.get("src")

        if not image_url or image_url.lower().split('.')[-1] not in files:
            continue

        full_url = urljoin(url, image_url)

        try:
            img_data = get(full_url).content
            img = open(BytesIO(img_data)).convert("RGB")
            #with open(rf"C:\Users\kavya\Downloads\Biology notes\11 class\11\{idx-1}.jpg", "wb") as f:
                #f.write(img_data)
            pil_images.append(img)
            #print(f"Fetched image {idx}: {full_url}")
        except Exception as e:
            print(f"\nFailed to load image: {full_url} — {e}")

    return pil_images, title


class insert_into_frame(Frame):
    def __init__(self, master, images, title: str, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.title = title
        self.images = images
        self.toggle_value = True
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame1 = Frame(self)
        self.frame1.grid(row=0, column=0, padx=3, pady=3, sticky='new')
        Button(self.frame1, text="Toggle All", command=self.toggle).grid(row=0, column=0, padx=3, sticky='w')
        Button(self.frame1, text="Save", command=self.on_ok).grid(row=0, column=1, padx=3, sticky='e')
        self.frame1.columnconfigure([0,1], weight=1)

        self.frame2 = ScrolledFrame(self, autohide=True)
        self.frame2.grid(row=1, column=0, sticky='nsew', padx=3, pady=3)
        self.frame2.columnconfigure(0, weight=1)

        self.tkimage = {}
        for idx, image in enumerate(images, 0):
            old_width, old_height = image.size
            i = PhotoImage(image.resize((600, round((600 / old_width) * old_height)), Resampling.BOX))
            v = BooleanVar(self, value=1)
            Checkbutton(self.frame2, cursor='hand2', text=str(idx+1), image=i, compound='right', onvalue=1, offvalue=0, variable=v).grid(column=0, row=idx, padx=(10,3), pady=3, sticky='ew')
            self.tkimage[idx] = [v, i, image]

    def on_ok(self):
        images = []
        for idx in self.tkimage.values():
            if idx[0].get():
                images.append(idx[2])
        try:
            if not images:
                raise FileNotFoundError("No image found.")
            images[0].save(self.title, save_all=True, append_images=images[1:])
            print(f"PDF created: {self.title}")
        except Exception as e:
            print(f"Failed to save PDF: {e}")
        finally:
            del images
            del self.tkimage
            root.destroy()
            exit()
    
    def toggle(self):
        if self.toggle_value:
            for i in self.tkimage.values():
                i[0].set(0)
            self.toggle_value=False
        else:
            for i in self.tkimage.values():
                i[0].set(1)
            self.toggle_value=True


def exit_fuct(images):
    del images
    del frame.tkimage
    root.destroy()
    exit()


if __name__ == "__main__":
    # Step 1: Extract images from URL
    url = input("enter url: ")
    if url.strip().lower() == "exit":
        exit()
    files = input("enter image extensions seprated by space\ndefault: jpg png webp\n==> ").split()
    files = files if files else ['webp', 'jpg', 'png', 'jpeg']
    images, title = extract_images_as_pil(url, files=files)
    title = sub(r'[\\/*?:"<>|]', "", title).strip() + ".pdf"

    name = input(f"enter name of pdf \n(leave empty for default name: \n{title}) \n==> ").strip()
    if name:
        if '.pdf' == name[-4:]:
            title = name
        else:
            title = name + '.pdf'

    root = Window(title=title, themename="darkly", size=(700, 500))
    root.wm_protocol("WM_DELETE_WINDOW",lambda: exit_fuct(images))

    frame = insert_into_frame(root, images, title)
    frame.pack(fill='both', expand=True)
    frame.focus_force()

    root.bind("<Return>", lambda event: frame.on_ok())

    if not images:
        print("no images found")
        exit_fuct(images)

    root.mainloop()