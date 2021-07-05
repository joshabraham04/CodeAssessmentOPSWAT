import hashlib
import requests
import sys

# INTRO AND INSTRUCTION PROMPT
print("Welcome to the file scanner using the OPSWAT API.")
print("To run the application, enter the filename.type when prompted to upload file.")
print("The application will loop indefinitely. To exit, press the keyboard interruption, \"CTRL+C\", at the prompt.")
print("------")
print()

# LOOP TO SCAN EACH FILE
while True:
    # CALCULATE FILE HASH (MD5)
    # -------------------------
    # input file name and extension
    try:
        fileName = input("upload_file ")
        print()
    except KeyboardInterrupt as exit:
        sys.exit("\nCTRL+C Pressed - Application terminated")
    file = "files/" + fileName
    BLOCK_SIZE = 65536
    file_hash = hashlib.md5()
    # hash file using method, catch any exceptions
    try:
        with open(file, 'rb') as f:
            fb = f.read(BLOCK_SIZE)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(BLOCK_SIZE)
    except:
        sys.exit("Invalid input, unable to read file. Check file name and extension.")

    hash = file_hash.hexdigest()

    # HASH LOOKUP
    # -------------------------
    # http request protocol variables
    param = {'apikey':sys.argv[1], 'content-type':''}
    lookupURL = 'https://api.metadefender.com/v4/hash/'
    scanURL = 'https://api.metadefender.com/v4/file/'

    # Get request for file data, raise any exceptions
    try:
        r = requests.get(lookupURL+hash, headers=param)
        r.raise_for_status()

    # Exception Handling
    # --------------------------
    except requests.HTTPError as exception:
        # Polling data for uncached files
        if r.status_code == 404:
            print("Uncached file. Polling file results now. This may take a while...\n")
            param['content-type']='application/octet-stream'
            upload = requests.post(scanURL, headers=param, data=open(file, 'rb'))
            dataID = upload.json()["data_id"]
            r = requests.get(scanURL+dataID, headers=param)
            scan_status = r.json()["scan_results"]["scan_all_result_a"]
            # repeated polling to retrieve all the data
            while scan_status=="In Progress" or scan_status=="In queue":
                r = requests.get(scanURL+dataID, headers=param)
                scan_status = r.json()["scan_results"]["scan_all_result_a"]

        # Handling for any other issues. Exits the programm
        elif r.status_code == 401:
            sys.exit("ERROR 401: Authentication Failed. Review API key.")
        elif r.status_code == 408:
            sys.exit("ERROR 408: Request Timeout. The request took too long.")
        elif r.status_code == 429:
            sys.exit("ERROR 429: Too Many Requests. The rate limit was exceeded.")
        elif r.status_code == 500:
            sys.exit("ERROR 500: Something went wrong with the API")
        elif r.status_code == 503:
            sys.exit("ERROR 503: Service Unavailable")
        else:
            sys.exit("Something went wrong...")

    # DISPLAY FORMATTED RESULTS
    # -------------------------
    print("filename:", fileName)
    print("overall_status:", r.json()['scan_results']['scan_all_result_a'])
    scan_details = r.json()['scan_results']['scan_details']
    for engine in scan_details:
        print("engine:", engine)
        print("threat_found:", scan_details[engine]['threat_found'])
        print("scan_result:", scan_details[engine]['scan_result_i'])
        print("def_time:", scan_details[engine]['def_time'])
    print("END \n")