from lxml import etree


def plant_catalog(zone):
    with open('plant_catalog.xml') as file:
        catalog = etree.parse(file)
    return catalog.xpath(f"//ZONE[text()='{zone}']/ancestor::PLANT")


if __name__ == '__main__':
    plants = plant_catalog('4')

    for plant in plants:
        print(f"COMMON: {plant.xpath('./COMMON')[0].text}")
        print(f"PRICE: {plant.xpath('./PRICE')[0].text}")
        print(f"AVAILABILITY: {plant.xpath('./AVAILABILITY')[0].text}")
