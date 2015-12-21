from datetime import datetime

from PIL import Image
from selenium import webdriver


def yield_position(x, y):
    for position in ((0, 0, x, y),
                     (x, 0, 2 * x, y),
                     (0, y, x, 2 * y),
                     (x, y, 2 * x, 2 * y)):
        yield position


def take_screenshot(newspapers):
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    for newspaper in newspapers:
        driver.get(newspaper[0])
        driver.get_screenshot_as_file(newspaper[1])
        print '{} screenshot taken'.format(newspaper[0])
    driver.quit()


if __name__ == '__main__':
    papers = (('http://www.theglobeandmail.com/', 'globe_and_mail.png'),
              ('http://www.thestar.com/', 'the_star.png'),
              ('http://www.cbc.ca/', 'cbc.png'),
              ('http://www.nationalpost.com/index.html', 'national_post.png'))
    take_screenshot(papers)
    crop_box = (0, 0, 1028, 829)
    mid_x, mid_y = crop_box[2:]
    new_front_image = Image.new('RGB', [dimension * 2 for dimension in (mid_x, mid_y)])
    images = (x[1] for x in papers)
    image_order = yield_position(mid_x, mid_y)
    for image in images:
        open_image = Image.open(image)
        open_image = open_image.crop(crop_box)
        open_image.save(image)
        new_front_image.paste(open_image, image_order.next())
    now = datetime.now()
    new_front_image.save('frontpage_{}_{}_{}.png'.format(now.year, now.month, now.day))

    print 'Finished'
