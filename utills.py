SEPERATORS = b"\\/[]<>()\t\n\r"

from io import BytesIO, SEEK_CUR, SEEK_SET, SEEK_END


class ObjectIter:

    def __init__(self, iterable: bytes, pointer=0):
        """
        :param iterable: Any object that supports __getitem__ ([index] operator)
        :param pointer: A pointer to the start index
        """
        self.iterable = BytesIO(iterable)
        self.iterable.seek(pointer)
        self.length = self.iterable.seek(0, SEEK_END)
        self.deb = iterable
        self.iterable.seek(0)
        self._clean()

    def _clean(self):
        """
        Increments the iterable to the next non space character
        """
        while self.peek(1).isspace():
            self.iterable.seek(1, SEEK_CUR)

    def _prepare_dictparse(self) -> None:
        """
        Moves the Pointer to the item preceding a forward slash /
        """
        self.move_to(b"/")

    def __len__(self):
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        byte = self.iterable.read(1)
        if (byte == b""):
            raise StopIteration
        return byte

    def prev(self) -> bytes:
        """
        Decrements the counter
        :return: Previous element
        """
        self.iterable.seek(-2, SEEK_CUR)
        return self.iterable.read(1)

    def move_pointer(self, n):
        self.iterable.seek(n, SEEK_CUR)

    def move_to(self, item):
        """
        Moves the iterator to given item
        :param item: item to move to
        :return: Items since the beginning of iteration till end
        """
        pointerStart = self.iterable.tell()
        nextbyte = self.peek(1)
        while nextbyte != item:
            if self.iterable.tell() == self.length:
                pointer = self.iterable.tell()
                self.iterable.seek(-1, SEEK_CUR)
                pointer = self.iterable.tell()
                countClosingBraces = 0
                curr = self.iterable.read(1)
                pointer = self.iterable.tell()
                while countClosingBraces != 2:
                    pointer = self.iterable.tell()
                    countClosingBraces += curr == b">"
                    self.iterable.seek(-2, SEEK_CUR)
                    curr = self.iterable.read(1)

                poiterEnd = self.iterable.tell()
                self.iterable.seek(pointerStart - poiterEnd, SEEK_CUR)
                return self.iterable.read(poiterEnd - pointerStart)
            if self.iterable.tell() <= self.length:
                self.iterable.read(1)
                nextbyte = self.peek(1)
                continue
            else:
                raise IndexError(f"{item} not found")

        poiterEnd = self.iterable.tell()
        self.iterable.seek(pointerStart - poiterEnd, SEEK_CUR)
        value = self.iterable.read(poiterEnd - pointerStart)
        return value

    def finish_number(self) -> bytes:
        """
        Move stream until a separating character is found
        :return: Resulting int
        """
        rest = b""
        for char in iter(self):
            if char in SEPERATORS:
                break
            rest += char
        self.prev()  # Move back in order to preserve type token for next item
        return rest

    def peek(self, n=1):
        """
        Returns the next n chars without incrementing the counter
        :param n: number of characters
        :return: Returns the next n chars without incrementing the counter
        """
        prepeak = self.iterable.tell()
        out_string = self.iterable.read(n)
        self.iterable.seek(prepeak)
        if (self.iterable.tell() == self.length):
            return out_string
        return out_string


class Ibytable:

    def itemToByte(self,item) -> bytes:
        try:
            return item.to_bytes()
        except AttributeError as E:
            # print(E)
            return bytes(item)


    def to_bytes(self):
        raise NotImplemented

    def __eq__(self, other):
        raise NotImplemented

    def offset_references(self,offset:int):
        raise NotImplemented

    def __repr__(self):
        return self.__str__()

