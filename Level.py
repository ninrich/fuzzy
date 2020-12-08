class Level:

    def __init__(self, name, a, b, alpha, beta):
        self.name = name
        self.beta = beta
        self.alpha = alpha
        self.b = b
        self.a = a

    def get_abcd(self):
        a = self.a - self.alpha
        b = self.a
        c = self.b
        d = self.b + self.beta
        return [a, b, c, d]

    def get_name(self):
        return self.name

    def get_maximum_value(self):
        return self.b + self.beta
