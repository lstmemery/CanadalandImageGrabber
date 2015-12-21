from selenium import webdriver
from PIL import Image
from datetime import datetime

def yield_position(x, y):
    for position in ((0, 0), (x, 0), (0, y), (x, y)):
        yield position

if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    newspapers = (('http://www.theglobeandmail.com/', 'globe_and_mail.png'),
                  ('http://www.thestar.com/', 'the_star.png'),
                  ('http://www.cbc.ca/', 'cbc.png'),
                  ('http://www.nationalpost.com/index.html', 'national_post.png'))
    for newspaper in newspapers:
        driver.get(newspaper[0])
        driver.get_screenshot_as_file(newspaper[1])
        print '{} screenshot taken'.format(newspaper)
    driver.quit()
    crop_box = (0, 0, 1028, 829)
    mid_x, mid_y = crop_box[2:]
    new_front_image = Image.new('RGB', [dimension * 2 for dimension in (mid_x, mid_y)])
    images = (x[1] for x in newspapers)
    image_order = yield_position(mid_x, mid_y)
    for image in images:
        open_image = Image.open(image)
        open_image = open_image.crop(crop_box)
        open_image.save(image)
        new_front_image.paste(image, image_order)
    now = datetime.now()
    new_front_image.save('frontpage_{}_{}_{}.png'.format(now.year, now.month, now.day))

    print 'Finished'
