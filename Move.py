from Converters import c2m, t2m


class Move:
    def __init__(self, fy: int, fx: int, ty: int, tx: int, key: str, mode: str, extra_info=None, notation=None):
        self.key = key
        self.fy = fy
        self.fx = fx
        self.ty = ty
        self.tx = tx
        self.mode = mode
        self.comment = ''
        self.extra_info = extra_info

    def add_comment(self, comment: str):
        self.comment = comment

    def __str__(self):
        if self.mode in ('0-0-0', '0-0'):
            return self.mode
        else:
            return self.key + c2m(self.fy, self.fx) + self.mode + c2m(self.ty, self.tx) + self.comment

    def __call__(self):
        return self.fy, self.fx, self.ty, self.tx
