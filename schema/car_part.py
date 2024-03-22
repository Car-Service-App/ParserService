class CarPart():
    name: str
    oem: str = "1"
    link: str
    image_link: str
    last_price: str

    def __str__(self):
        return f"name: {self.name} oem: {self.oem} link: {self.link} image_link: {self.image_link} last_price: {self.last_price}"
