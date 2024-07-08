def image_formater(image : str, db) -> str:
    '''
    Automaticly format image to correct format
    '''
    # If not image, add image with same id as post    
    if not image:
        id = db.execute_file('sql_scripts/select/last_post_id.sql')[0][0] + 1
        image = '/static/images/' + str(id) + '.jpg'
    
    # If image is '-', remove it and leave empty
    if image == '-':
        image = ''

    # If image is not in any folder, add it to '/static/images/'
    if not '/' in image and image:
        image = '/static/images/' + image
    
    return image