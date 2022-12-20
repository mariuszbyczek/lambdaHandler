import json
import csv
import boto3


# nalezy miec skonfigurowanego localstacka albo wlasny bucket
# w buckecie znajduja sie juz pliki

def lambda_handler(event):
    s3 = boto3.client('s3')
    color_data = []

#pobieramy CSV-ki i tworzymy plik json
    for file_name in event['files']:
        csv_content = s3.get_object(Bucket="bucket", Key=f'csv-files/{file_name}')['Body'].read().decode()
        reader = csv.DictReader(csv_content.splitlines())
        for row in reader:
            color_hex = row['value']
            color_data.append({
                'name': row['color'],
                'hex': color_hex,
            })

    json_data = json.dumps(color_data)
    #pushujemy plik json do bucketa
    boto3.client('s3').put_object(Bucket='bucketName', Key='json-files/colors.json', Body=json_data)

    # out zapisze string do zwrocenia
    output = ''
    for color in color_data:
        output = output + f'{color["name"]}: #{color["hex"]} \n'

    return output


if __name__ == '__main__':
    file_names = ['example.csv', 'example1.csv', 'example2.csv']
    print(lambda_handler({'files': file_names}))
