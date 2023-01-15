# --- Optional functions specified by flags ---
import re
import shutil


def create_opf(metadata, opf_template):
    # --- Generate .opf Metadata file ---

    with opf_template.open('r') as file:
        template = file.read()

    # - Author -
    if metadata['author'] == '__unknown__':
        template = re.sub(r"__AUTHOR__", '', template)
    else:
        template = re.sub(r"__AUTHOR__", metadata['author'], template)

    # - Title -
    if metadata['title'] == metadata['input_folder']:
        template = re.sub(r"__TITLE__", '', template)
    else:
        template = re.sub(r"__TITLE__", metadata['title'], template)

    # - Summary -
    template = re.sub(r"__SUMMARY__", metadata['summary'], template)

    # - Subtitle -
    template = re.sub(r"__SUBTITLE__", metadata['subtitle'], template)

    # - Narrator -
    template = re.sub(r"__NARRATOR__", metadata['narrator'], template)

    # - Publisher -
    template = re.sub(r"__PUBLISHER__", metadata['publisher'], template)

    # - Publish Year -
    template = re.sub(r"__PUBLISHYEAR__", metadata['publishyear'], template)

    # - Genres -
    template = re.sub(r"__GENRES__", metadata['genres'], template)

    # - ISBN -
    template = re.sub(r"__ISBN__", metadata['isbn'], template)

    # - ASIN -
    template = re.sub(r"__ASIN__", metadata['asin'], template)

    # - Series -
    template = re.sub(r"__SERIES__", metadata['series'], template)

    # - Volume Number -
    template = re.sub(r"__VOLUMENUMBER__", metadata['volumenumber'], template)

    opf_output = metadata['final_output'] / 'metadata.opf'
    with opf_output.open('w', encoding='utf-8') as file:
        file.write(template)

    return


def create_info(metadata):
    # --- Generate info.txt summary file ---
    txt_file = metadata['final_output'] / 'info.txt'
    with txt_file.open('w', encoding='utf-8') as file:
        file.write(metadata['summary'])

def flatten_folder(metadata, log):
    # --- Flatten folder and rename audio files to avoid conflicts ---

    # - Get all audio files -
    audio_ext = ['mp3', 'm4b', 'm4a', 'ogg']
    audio_files = []
    for extension in audio_ext:
        results = sorted(metadata['final_output'].rglob(f"./*.{extension}"))
        for result in results:
            if result.parent != metadata['final_output']:
                audio_files.append(result)

    # - Sort files for renaming
    audio_files.sort()
    log.debug(f"Globbed audio files for flattening = {str(audio_files)}")

    # - Move all audio files to root of book folder -
    track = 1
    padding = 2
    if len(audio_files) >= 100:
        padding = 3

    for file in audio_files:
        file.rename(metadata['final_output'] / f"{str(track).zfill(padding)} - {metadata['title']}{file.suffix}")
        log.debug(metadata['final_output'] / f"{str(track).zfill(padding)} - {metadata['title']}{file.suffix}")
        track += 1

    # - Delete old folders -
    for file in audio_files:
        if file.parent != metadata['final_output']:
            shutil.rmtree(file.parent, ignore_errors=True)

    return
