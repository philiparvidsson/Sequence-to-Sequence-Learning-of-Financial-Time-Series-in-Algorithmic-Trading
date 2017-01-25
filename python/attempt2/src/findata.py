#---------------------------------------
# CONSTANTS
#---------------------------------------

TIME      = 0
OPEN_ASK  = 1
OPEN_BID  = 2
HIGH_ASK  = 3
HIGH_BID  = 4
LOW_ASK   = 5
LOW_BID   = 6
CLOSE_ASK = 7
CLOSE_BID = 8
VOLUME_ASK = 9
VOLUME_BID = 10

#---------------------------------------
# CLASSES
#---------------------------------------

class DataRow(object):
    def __init__(self, args):
        self.raw = args

    @property
    def time(self): return self.raw[TIME]

    @property
    def open_ask(self): return self.raw[OPEN_ASK]

    @property
    def open_bid(self): return self.raw[OPEN_BID]

    @property
    def high_ask(self): return self.raw[HIGH_ASK]

    @property
    def high_bid(self): return self.raw[HIGH_BID]

    @property
    def low_ask(self): return self.raw[LOW_ASK]

    @property
    def low_bid(self): return self.raw[LOW_BID]

    @property
    def close_ask(self): return self.raw[CLOSE_ASK]

    @property
    def close_bid(self): return self.raw[CLOSE_BID]

    @property
    def volume_ask(self): return self.raw[VOLUME_ASK]

    @property
    def volume_bid(self): return self.raw[VOLUME_BID]

class DataSet(object):
    def __init__(self, rows):
        self.num_rows = len(rows)
        self.rows     = rows

    def to_array(self):
        a = []

        for row in self.rows:
            a.extend(row.raw)

        return a

    def transform(self, *cols):
        data = []

        for i in range(self.num_rows):
            row = []

            for col in cols:
                row.append(self.rows[i].raw[col])

            data.append(row)

        return data
