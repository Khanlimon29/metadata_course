import exifread

def extract_metadata(image):
    try:
        with open(image, 'rb') as f:
            tags = exifread.process_file(f)       
            for tag, value in tags.items():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                    print(f"{tag}: {value}")
            return tags
    except Exception as e:
        return f"Ошибка: {str(e)}"

if __name__ == "__main__":
    image = "IMG_0059.CR2"
    result = extract_metadata(image)


