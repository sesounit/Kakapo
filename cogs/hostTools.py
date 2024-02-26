import nextcord, os.path, json, datetime
from nextcord.ext import commands, tasks
from datetime import datetime

class hostTools(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.database2 = {'notifications' : {}}
        self.roster_category = None

    def cog_unload(self):
        self.sendNotification.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        #Set global variable for channels
        # Because of the funny icons in Dogegs we have to use the ID of the channel 451858500784619550
        # Because of the funny icons in Monkeys we have to use the ID of the channel 911066596456415269
        global hostNotificationsChannel
        global dogegsChannel
        global botCommandsChannel 
        botCommandsChannel = nextcord.utils.get(self.client.get_all_channels(), name=f"bot-commands")
        dogegsChannel = nextcord.utils.get(self.client.get_all_channels(), id=911066596456415269)
        hostNotificationsChannel = nextcord.utils.get(self.client.get_all_channels(), name=f"host-notifications")
        #Check and load pre-existing roster JSON
        if os.path.exists('autoSlot.json'):
            with open('autoSlot.json', 'r') as json_file:
                self.database = self.client.get_cog('autoSlot').database
        if os.path.exists('autoNotifications.json'):
            with open('autoNotifications.json', 'r') as json_file2:
                self.database2 = json.load(json_file2)
        self.sendNotification.start()


    @commands.command(name = "addEvent", help = "Adds a discord event for a specific operation")
    async def addEvent(self, ctx, operation_id):

        ''' 
        Created 1-18-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * Create a discord event for Arma Operations
        
        -- Logic -- 
        * Grab and Format all inputs
        * Check if the event already exists
        * Create event using nextcord's ctx.guild.create_scheduled_event()
        * Send notification
        
        -- Error Prevention -- 
        * Validate operation ID is valid
        * Prevent event creation if event already exists
        '''

        # Check if operation ID exists
        if await checkOpID(self, operation_id) is not None: return
        
        # Grab variables required to create the scheduled event
        nameInput=f"{self.database['operations'][operation_id]['name']}"
        entity_typeInput = nextcord.ScheduledEventEntityType.voice
        start_timeInput = datetime.utcfromtimestamp(int(self.database['operations'][operation_id]['operation_timestamp']))
        channelInput = dogegsChannel
        end_timeInput = datetime.utcfromtimestamp(int(self.database['operations'][operation_id]['operation_timestamp']) + 7200)

        # Check if start time is in the past as it will fail to complete if it is
        if await checkIfTimeIsInThePast(start_timeInput) is not None: return

        # Generate discord event using pre-defined variables if event with same name doesnt exist
        if (await eventExists(ctx, nameInput)): 
            await botCommandsChannel.send("Event for " + nameInput + " already exists")
        else: 
            await ctx.guild.create_scheduled_event(name = nameInput, entity_type = entity_typeInput, start_time = start_timeInput, channel = channelInput, end_time = end_timeInput, description = nameInput)
            await botCommandsChannel.send("Event " + nameInput + " created")

        

    @commands.command(name = "addReminder", help = "Schedule a reminder to ping a Host")
    async def addReminder(self, ctx, user, notifTime, notifMessage = None, operation_id = None):
        
        ''' 
        Created 1-19-2024 by Chief
        Updated 2-25-2024 by Chief

        -- Purpose -- 
        * Create a reminder to ping Arma Operation Hosts at specific times

        -- Logic -- 
        * Loop through a json file containing the notifications every minute using nextcord's @tasks.loop(seconds = 60.0)
        * If the notification time of the file is greater than the current time, send the notification and delete the entry
        * Else proceed to next entry

        -- Json File Format --
        Notification Timestamp (In Unix Seconds), Member_ID to ping, Notification Message, Operation ID (If applicable)

        -- Error Prevention -- 
        * Validate User Input
        * If json does not exist create a new one
        '''

        # Check if operation ID exists, ignore if the operation ID input is null
        if (operation_id is not None) and (await checkOpID(self, operation_id) is not None): return

        # Check if user exists
        if await checkIfUserExists(ctx, user) is not None: return

        # Validate input is a number
        if await checkIfIntNumber(notifTime) is not None: return

        # Loop through json and find the lowest value notification ID available
        notificationID = 1
        while notificationID < 1000:
            if str(notificationID) not in self.database2['notifications'] :
                break
            else:
                notificationID += 1

        # Add row to json with input data and save the file
        self.database2['notifications'].update({str(notificationID) : {'User': user, 'Time': notifTime, 'Message': notifMessage, 'Operation ID': operation_id}})
        saveJsonData(self)
        formattedTime = "<t:" + str(notifTime) + ":F>"
        if (operation_id is not None):
            await hostNotificationsChannel.send(f"Notification created for {user} at {formattedTime} with message \"{notifMessage}\" for operation ID {operation_id}")
        else:
            await botCommandsChannel.send(f"Notification created for {user} at {formattedTime} with message \"{notifMessage}\"")

        
    @commands.command(name = "deleteReminder", help = "Delete a reminder")
    async def deleteReminder(self, ctx, notificationID: str):
        ''' 
        Created 1-21-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * Delete a specific reminder from the autoNotifications json

        -- Logic -- 
        * Grab data from the json before the data is deleted
        * Based on the user input for notification ID, delete that specific entry
        * Send deletion notification message
        '''

        # Validate input is a number
        if await checkIfIntNumber(notificationID) is not None: return

        # Grab data from message before deletion
        messageToSend = f"Notification created for {self.database2['notifications'][notificationID]['User']} at {self.database2['notifications'][notificationID]['Time']} removed"

        # Delete value from internal DB
        del self.database2['notifications'][notificationID]
        saveJsonData(self)
        await botCommandsChannel.send(messageToSend)

    @commands.command(name = "listReminders", help = "Delete a reminder")
    async def listReminders(self, ctx):
        ''' 
        Created 1-21-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * List all the reminders stored in the autoNotifications json

        -- Logic -- 
        * Looping through the json
        * Format the time in the long discord time format
        * Send notification to bots channel
        '''

        # Loop through notification DB and send the list to the bots command channel
        for notificationID in self.database2['notifications'].copy():
            user = ctx.guild.get_member(int(self.database2['notifications'][notificationID]['User'].translate({ord(i): None for i in '@<>'})))
            time = "<t:" + str(self.database2['notifications'][notificationID]['Time']) + ":F>"
            await botCommandsChannel.send(f"Notification {notificationID}: {user} {time} {self.database2['notifications'][notificationID]['Message']}")


    @tasks.loop(seconds=60)
    async def sendNotification(self):
        ''' 
        Created 1-21-2024 by Chief
        Updated 1-22-2024 by Chief

        -- Purpose -- 
        * Send notifications for pre-defined reminders

        -- Logic -- 
        * Every 60 seconds go through the autoNotifications json
        * If the notification time is less than the current time, send notification and delete the entry
        '''
         
        currentUTCTime = datetime.utcnow()
        # Every 60 seconds loop through the notification DB by creating a temp copy of the DB and comparing the timestamp of the current time to the time in the DB
        for notificationID in self.database2['notifications'].copy():
            if datetime.utcfromtimestamp(int(self.database2['notifications'][notificationID]['Time'])) < currentUTCTime:
                if (self.database2['notifications'][notificationID]['Operation ID'] is not None):
                    await hostNotificationsChannel.send(f"{self.database2['notifications'][notificationID]['User']} {self.database2['notifications'][notificationID]['Message']}")
                else:
                    await botCommandsChannel.send(f"{self.database2['notifications'][notificationID]['User']} {self.database2['notifications'][notificationID]['Message']}")
                del self.database2['notifications'][notificationID]
                saveJsonData(self)

    # Required for sendNotification loop
    @sendNotification.before_loop
    async def beforeSendNotification(self):
        await self.client.wait_until_ready()


# Functions
def saveJsonData(self):
    # Dumps data to autoSlot.json
    with open('autoNotifications.json', 'w') as f:
        json.dump(self.database2, f)

async def eventExists(ctx, nameInput):
    # Loop through active events and if the name of the event is identical to the name of the operation, return True
    async for event in ctx.guild.fetch_scheduled_events():
        if (event.name == nameInput):
            return True
        else:
            False

async def checkIfUserExists(ctx, userToVerify):
    # If the input is not a valid user, return message
    try:
        ctx.guild.get_member(int(userToVerify.translate({ord(i): None for i in '@<>'})))
    except:
        print(f"Failed to find user with id {userToVerify}")
        return await botCommandsChannel.send(f"{userToVerify} Invalid User, please make sure its an @User mention")
    return None

async def checkIfIntNumber(numberToVerify):
    # If the input is not a number, return message
    try:
        val = int(numberToVerify)
    except:
        print(f"Value failed to verify as an int {numberToVerify}")
        return await botCommandsChannel.send(f"{numberToVerify} Invalid Number, please make sure its a whole number")
    return None

async def checkOpID(self, operation_id):
    # If operation with this ID does not exist, return message
    try:
        if operation_id not in self.database['operations']:
            return await botCommandsChannel.send("There is no operation present in the database with this ID.")
    except:
        print(f"Value failed to verify as an operation ID {operation_id}")
        return await botCommandsChannel.send("A problem occured with the operation id.")
    return None

async def checkIfTimeIsInThePast(inputTime):
    # If operation with this ID does not exist, return message
    currentTime = datetime.utcnow()
    if (currentTime > inputTime):
        print(f"Time found to be in the past current Time = {currentTime}, input Time = {inputTime}")
        return await botCommandsChannel.send(f"{inputTime} Is in the past, please make sure its greater than the current time {currentTime}")
    else:
        return None
    
async def deleteUserMessage(ctx):
    try:
        await ctx.message.delete()
    except:
        print()

async def silentPingSingleUser(inputMessage, user):
    await inputMessage.edit(user + " " + inputMessage.content)
    
def setup(client):
    client.add_cog(hostTools(client))



    '''
    Questions:
    What Channel do we want the bot to post reminders into: Host Notifications
    Who do we want to be able to create reminders: Anyone
    How often do we want to loop: 60 second
    What other functions should we add

    When do we want to ping Hosts /
    Do we want the event/reminders automatically created when a roster is posted /
    Events: Yes
    Reminders: 72hours, 24hours, 1hour
    '''