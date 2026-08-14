import os
import xml.etree.ElementTree as ET
import glob

# UA-DETRAC Class Mapping
CLASS_MAP = {
    'car': 0,
    'bus': 1,
    'van': 2,
    'others': 3
}

def convert_bbox_to_yolo(size, box):
    """Converts bounding box to YOLO normalized format (x_center, y_center, width, height)"""
    dw = 1. / size[0]
    dh = 1. / size[1]
    
    # Calculate center coordinates
    x_center = box[0] + (box[2] / 2.0)
    y_center = box[1] + (box[3] / 2.0)
    
    # Normalize
    x = x_center * dw
    y = y_center * dh
    w = box[2] * dw
    h = box[3] * dh
    return (x, y, w, h)

def parse_detrac_xml(xml_file, output_dir, img_width=960, img_height=540):
    """Parses UA-DETRAC XML and generates YOLO .txt annotation files, respecting ignore regions."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    sequence_name = root.attrib.get('name')
    
    # Iterate through every frame in the video sequence
    for frame in root.findall('frame'):
        frame_num = frame.attrib.get('num')
        target_list = frame.find('target_list')
        
        # Determine the YOLO .txt file name
        txt_filename = os.path.join(output_dir, f"{sequence_name}_img{frame_num.zfill(5)}.txt")
        
        with open(txt_filename, 'w') as out_file:
            if target_list is not None:
                for target in target_list.findall('target'):
                    # Filter out ignored regions
                    if target.find('attribute').attrib.get('vehicle_type') == 'ignored':
                        continue
                        
                    vehicle_type = target.find('attribute').attrib.get('vehicle_type')
                    if vehicle_type not in CLASS_MAP:
                        continue
                        
                    class_id = CLASS_MAP[vehicle_type]
                    box = target.find('box')
                    
                    # UA-DETRAC provides left, top, width, height
                    bbox = [
                        float(box.attrib['left']),
                        float(box.attrib['top']),
                        float(box.attrib['width']),
                        float(box.attrib['height'])
                    ]
                    
                    # Convert to YOLO format
                    yolo_bbox = convert_bbox_to_yolo((img_width, img_height), bbox)
                    
                    # Write to file
                    out_file.write(f"{class_id} {' '.join(map(str, yolo_bbox))}\n")

if __name__ == "__main__":
    print("UA-DETRAC to YOLO Conversion Script Initialized.")
    # In Colab, we will set these paths to our downloaded dataset directories
    # parse_detrac_xml('path/to/xml', 'path/to/output_labels')