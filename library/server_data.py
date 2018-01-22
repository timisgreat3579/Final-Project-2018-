from .loading_screen import session_var,user_login
from configparser import ConfigParser
from boto3.dynamodb.conditions import Key, Attr

session = session_var
people_table = session.Table('people')

def get_players(query):
    response = people_table.scan()
    names = []
    for i in response['Items']:
        name = i['peopleid']
        if query in name.lower() and len(query) is not 0:
            names.append(name)
        elif len(query) is 0:
            names.append(name)
    if user_login in names: names.remove(user_login)
    return names

def get_table_data(data):
    names = []
    response = people_table.query(KeyConditionExpression=Key('peopleid').eq(user_login))
    for i in response['Items']: names = i[data]
    if user_login in names: names.remove(user_login)
    return names

def get_game_data(game,data_type,target_user):
    game_table = session.Table(data_type)
    response = game_table.query(KeyConditionExpression=Key('peopleid').eq(target_user))
    for i in response['Items']: names = i[game]
    return names 

def accept_friend_request(friend):
    response = people_table.get_item(
        Key={
            'peopleid': user_login
        }
    )
    nFriends = response['Item']['friends']
    nFriends.append(friend)
    
    response = people_table.update_item(
        Key={
            'peopleid':user_login
        },
        UpdateExpression="set " + 'friends' + " = :r",
        ExpressionAttributeValues={
            ':r': nFriends,
        }
    )

    response = people_table.get_item(
        Key={
            'peopleid': friend
        }
    )
    nFreinds = response['Item']['friends']
    nFreinds.append(user_login)
    
    response = people_table.update_item(
        Key={
            'peopleid':friend
        },
        UpdateExpression="set " + 'friends' + " = :r",
        ExpressionAttributeValues={
            ':r': nFreinds,
        }
    )

    #update requests

    decline_friend_request(friend)
    

def decline_friend_request(friend):
    response = people_table.get_item(
    Key={
        'peopleid': friend
        }
    )
    oldRequests = response['Item']['requests']
    x = oldRequests.index(user_login)
    del oldRequests[x]
    
    response = people_table.update_item(
        Key={
            'peopleid':friend
        },
        UpdateExpression="set " + 'requests' + " = :r",
        ExpressionAttributeValues={
            ':r': oldRequests,
        }
    )

    response = people_table.get_item(
        Key={
            'peopleid': user_login
        }
    )
    oldRequests = response['Item']['requests']
    x = oldRequests.index(friend)
    del oldRequests[x]
    
    response = people_table.update_item(
        Key={
            'peopleid':user_login
        },
        UpdateExpression="set " + 'requests' + " = :r",
        ExpressionAttributeValues={
            ':r': oldRequests,
        }
    )
    

def send_friend_request(friend):
    response = people_table.get_item(
        Key={
            'peopleid': user_login
        }
    )
        
    oldRequests = response['Item']['requests']
    oldRequests.append(friend)
    
    response = people_table.update_item(
        Key={
            'peopleid':user_login
        },
        UpdateExpression="set " + 'requests' + " = :r",
        ExpressionAttributeValues={
            ':r': oldRequests,
        }
    )

    response = people_table.get_item(
        Key={
            'peopleid': friend
        }
    )
    oldRequests = response['Item']['requests']
    oldRequests.append(user_login)
    
    response = people_table.update_item(
        Key={
            'peopleid':friend
        },
        UpdateExpression="set " + 'requests' + " = :r",
        ExpressionAttributeValues={
            ':r': oldRequests,
        }
    )

def remove_friend(friend):
    pass
