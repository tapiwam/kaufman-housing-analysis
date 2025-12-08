
with open('/Users/tapiwamaruni/Documents/projects/housing1/Kaufman-CAD-2025-Certified-Full-Roll-Download-updated-with-Supp-5/2025-10-27_002174_APPRAISAL_INFO.TXT', 'r', encoding='latin1') as f:
    line = f.readline()
    print(f"Line length: {len(line)}")
    
    search_str = "BARAY RAUL ANTONIO"
    pos = line.find(search_str)
    print(f"'{search_str}' found at index: {pos} (0-based)")
    
    search_str_2 = "1823 BALMORAL DR"
    pos_2 = line.find(search_str_2)
    print(f"'{search_str_2}' found at index: {pos_2} (0-based)")

    search_str_3 = "CARROLLTON"
    pos_3 = line.find(search_str_3)
    print(f"'{search_str_3}' found at index: {pos_3} (0-based)")
    
    search_str_4 = "FM RD 2578"
    pos_4 = line.find(search_str_4)
    print(f"'{search_str_4}' found at index: {pos_4} (0-based)")
    
    search_str_6 = "99.0001.0000.0005.00.06.00"
    pos_6 = line.find(search_str_6)
    print(f"'{search_str_6}' found at index: {pos_6} (0-based)")
    
    # Check what is before it
    print(f"Chars before geo_id: '{line[pos_6-20:pos_6]}'")
