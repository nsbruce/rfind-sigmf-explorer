# from rfinder.types import Box
# from pathlib import Path
# import csv

# def load_csv_boxes(path: Path) -> list[Box]:
#     boxes: list[Box] = []
#     with open(path, 'r') as f:
#         try:
#             reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
#         except Exception as e:
#             print(f'Error reading {path} as floats: {e}')
#         next(reader)  # skip header
#         for row in reader:
#             # for row in islice(reader, 1, None):
#             try:
#                 boxes.append(Box(row))
#             except Exception as e:
#                 print(f'Error creating Box from {row}: {e}')
#     return boxes

# def bb_starst_end
    # boxes = load_csv_boxes(csv_path)
    # boxes.sort(key=lambda x: x.cy-x.h/2)
    # ts_start = int(math.floor(boxes[0].cy-boxes[0].h/2))
    # boxes.sort(key=lambda x: x.cy+x.h/2, reverse=True)
    # ts_end = int(math.ceil(boxes[0].cy+boxes[0].h/2))

    # print("tstart is ", ts_start)
    # print("tend is ", ts_end)
