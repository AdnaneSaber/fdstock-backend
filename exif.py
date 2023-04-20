import exifread

# Open image file for reading (binary mode)
with open('images/andrew-haimerl-NzPvxNSMXyg-unsplash.jpg', 'rb') as f:
    # Get EXIF tags
    tags = exifread.process_file(f)

    # Print all tags
    for tag in tags.keys():
        print(tag, tags[tag])