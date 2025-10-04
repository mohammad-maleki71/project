from kavenegar import *



def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('304A49354735466F6A6D35324E324244713046364F63574E5473614E5741374244324371314E33647775303D')
        params = {'sender': '2000660110', 'receptor': phone_number, 'message': f'{code} کد تایید شما '}
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


