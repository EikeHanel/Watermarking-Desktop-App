from tkinter import *
from tkinter import filedialog
import shutil
from PIL import Image, ImageTk

YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WATERMARK = Image.open("watermark.png")
SAVE_NAME = ""
MY_IMAGE = None
DISPLAY_IMAGE = None


def browse_files():
    global MY_IMAGE, DISPLAY_IMAGE, SAVE_NAME
    find_file_path = filedialog.askopenfilename(initialdir="Desktop",
                                                title="Select a File",
                                                filetypes=(("Image files",
                                                            ["*.jpg*", "*.png*", "*jpeg*"]),
                                                           ("all files",
                                                            "*.*")))
    file_path = shutil.copy2(find_file_path, "C:/Python/day-85-Portfolio_GUI_watermarking_desktop_app/")
    SAVE_NAME = find_file_path.split("/")[-1].split(".")[0]
    # Open and resize the image
    MY_IMAGE = Image.open(file_path)
    image_resize = MY_IMAGE
    # Resize the image to fit within the window
    if (image_resize.height - canvas_height) > (image_resize.width - canvas_width):
        if (image_resize.height - canvas_height) <= 0:
            image_resize = image_resize
        else:
            image_resize = image_resize.resize((int(image_resize.width * (canvas_width / image_resize.height)),
                                                int(image_resize.height * (canvas_width / image_resize.height))))
    elif (image_resize.height - canvas_height) <= (image_resize.width - canvas_width):
        if (image_resize.width - canvas_width) <= 0:
            image_resize = image_resize
        else:
            image_resize = image_resize.resize((int(image_resize.width * (canvas_height / image_resize.height)),
                                                int(image_resize.height * (canvas_height / image_resize.height))))
    # Convert the resized image to PhotoImage format
    DISPLAY_IMAGE = ImageTk.PhotoImage(image_resize)
    # Update the image on the canvas
    canvas.delete(canvas_text)
    canvas_img = canvas.create_image(canvas_width / 2, canvas_height / 2, image=DISPLAY_IMAGE)


def add_watermark(bg_img, fg_img, alpha=200):
    global MY_IMAGE

    if MY_IMAGE is not None:
        # Ensure bg_img is in RGBA mode and apply overall alpha
        bg_img = bg_img.convert('RGBA')
        # Resize the watermark to match the size of the background image
        fg_img = fg_img.resize(bg_img.size)
        # Adjust alpha channel of the watermark image
        fg_img.putalpha(fg_img.getchannel('A').point(lambda p: p * alpha // 255))
        # Calculate the position to center the watermark on the background image
        bg_width, bg_height = bg_img.size
        fg_width, fg_height = fg_img.size
        position = ((bg_width - fg_width) // 2, (bg_height - fg_height) // 2)
        # Paste the fg_img onto bg_img
        bg_img.paste(fg_img, position, fg_img)
        # Save the result to a file
        bg_img.save(f"Watermarked - {SAVE_NAME}.png")
        # Display the image
        bg_img.show()


# ---------------------------- UI SETUP ------------------------------- #
# INFO Window
# Create the root window
window = Tk()

# Set window title
window.title('Watermark')

# Set window background color
window.config(padx=50, pady=50, bg=YELLOW)

# Defining and create the canvas!
canvas_height = 300
canvas_width = 400
canvas = Canvas(width=canvas_width, height=canvas_height, bg=YELLOW, highlightthickness=0)
canvas_text = canvas.create_text(canvas_width/2, canvas_height/2, text="Add a Watermark", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

# Explore Button: Search and load an image
button_explore = Button(window,
                        text="Load Image",
                        command=browse_files)
button_explore.grid(column=1, row=3, pady=50)
# Watermark Button: Adding the Watermark onto the Image
button_watermark = Button(window,
                          text="Add Watermark",
                          command=lambda: add_watermark(MY_IMAGE, WATERMARK))
button_watermark.grid(column=1, row=4, pady=50)

button_exit = Button(window,
                     text="Exit",
                     command=exit)
button_exit.grid(column=1, row=6)

# Let the window wait for any events
window.mainloop()
