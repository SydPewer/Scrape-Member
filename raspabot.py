from datetime import datetime, timedelta
import os, json, asyncio, sys
from telethon import TelegramClient, events, Button
from telethon.sync import TelegramClient as TMPTelegramClient
from telethon.errors import PhoneNumberFloodError, SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest, UpdateProfileRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from telethon.tl.functions.photos import UploadProfilePhotoRequest

ADMIN = # Your ID

API_KEY =  #api id
API_HASH = ""
STRING_SESSION = ""
ADMINS = []
Getter = None
Number = None
TempClient = None
Grab = None
activeusers = False
inAdding = False
canAdd = True
maxusers = 0
AddedUsers = []
tentativi = 0
countusers = 0
raspingintelligentelist = {}
if os.path.exists("SSs.json"):
    with open("SSs.json", "r+") as f:
        SSs = json.load(f)
else:
    SSs = {}
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)

if os.path.exists("ArchSSs.json"):
    with open("ArchSSs.json", "r+") as f:
        ArchSSs = json.load(f)
else:
    ArchSSs = {}
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)


def saveSS():
    global SSs
    with open("SSs.json", "w+") as f:
        json.dump(SSs, f)


def saveArchSS():
    global ArchSSs
    with open("ArchSSs.json", "w+") as f:
        json.dump(ArchSSs, f)


async def addUsers(client, Users, group):
    global canAdd, AddedUsers, countusers, maxusers, tentativi
    AddedUsers = []
    tentativi = 0
    for user in Users:
        if maxusers == 0:
            if canAdd:
                AddedUsers.append(user)
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    await asyncio.sleep(0.2)
                    countusers = countusers + 1
                except:
                    tentativi = tentativi + 1
                    pass
            else:
                break
        elif maxusers > 0 and countusers < maxusers:
            if canAdd:
                AddedUsers.append(user)
                try:
                    await client(InviteToChannelRequest(group, [user]))
                    await asyncio.sleep(0.2)
                    countusers = countusers + 1
                except:
                    tentativi = tentativi + 1
                    pass
            else:
                break


async def timeoutAdd(timeout):
    global canAdd
    await asyncio.sleep(timeout)
    canAdd = False


print("\033[Decrease the control of other admins for seller settings? [Y/N]: (by argument)")
try:
    controllolimitato = sys.argv[1].upper().startswith("Y")
except:
    controllolimitato = True
    print("Limited seller control: True, no arguments passed. e.g.: python3 nomescript.py N")
bot = TelegramClient("bot", API_KEY, API_HASH)
archivialimitati = True
def raspacontrol():
    global raspingintelligentelist, ArchSSs
    R53 = False
    for voipdacontrollare in raspingintelligentelist:
        if datetime.now().date()> raspingintelligentelist[voipdacontrollare].date():
            R53 = True
            SSs[voipdacontrollare] = ArchSSs[voipdacontrollare]
            saveSS()
            del (ArchSSs[voipdacontrollare])
            saveArchSS()
    return R53

@bot.on(events.NewMessage(incoming=True))
async def RaspaManager(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, canAdd, AddedUsers, ADMINS, controllolimitato, countusers, activeusers, maxusers, tentativi,archivialimitati, raspingintelligentelist
    if e.is_private:
        if e.chat_id == ADMIN or e.chat_id in ADMINS:
            if e.text == "/start":
                Getter, Number, TempClient = None, None, None
                if archivialimitati:
                    if raspacontrol():
                        await e.respond("**OF THE VOIPS HAVE BEEN RE-ADDEDn🤖 Raspa Panel Bot\n\n⚙ Version » 4.4**",
                                        buttons=[[Button.inline("📞 Voip", "voip")],
                                                 [Button.inline("👥 Steal", "grab"), Button.inline("✔ Add", "add")],
                                                 [Button.inline("🎛️ADMIN PANEL", "adminpanel")]])
                    else:
                        await e.respond("**OF THE VOIPS HAVE BEEN RE-ADDEDn🤖 Raspa Panel Bot\n\n⚙ Version » 4.4**",
                                        buttons=[[Button.inline("📞 Voip", "voip")],
                                                 [Button.inline("👥 Steal", "grab"), Button.inline("✔ Add", "add")],
                                                 [Button.inline("🎛️ADMIN PANEL", "adminpanel")]])
                else:
                    await e.respond("**OF THE VOIPS HAVE BEEN RE-ADDEDn🤖 Raspa Panel Bot\n\n⚙ Version » 4.4**",
                                    buttons=[[Button.inline("📞 Voip", "voip")],
                                             [Button.inline("👥 Steal", "grab"), Button.inline("✔ Add", "add")],
                                             [Button.inline("🎛️ Admin Panel", "adminpanel")]])

            elif Getter != None:
                if Getter == 0:
                    Getter = None
                    if not e.text in SSs:
                        if not e.text in ArchSSs:
                            TempClient = TMPTelegramClient(StringSession(), API_KEY, API_HASH)
                            await TempClient.connect()
                            try:
                                await TempClient.send_code_request(phone=e.text, force_sms=False)
                                Number = e.text
                                Getter = 1
                                await e.respond("**📩 Enter the code 📩**",
                                                buttons=[[Button.inline("❌ Cancel", "voip")]])
                            except PhoneNumberFloodError:
                                await e.respond("**❌ Too many attempts! Try another number ❌**",
                                                buttons=[[Button.inline("🔄 Try again", "addvoip")]])
                            except:
                                await e.respond("**❌ Not valid nummber ❌**",
                                                buttons=[[Button.inline("🔄 Try again", "addvoip")]])
                        else:
                            await e.respond("**❌ Archived Voip! Re-add His ❌**",
                                            buttons=[[Button.inline("📁 Archived Voip", "arch")],
                                                     [Button.inline("🔄 Try again", "addvoip")]])
                    else:
                        await e.respond("**❌ Voip already added ❌**", buttons=[[Button.inline("🔄 Try Again", "addvoip")]])
                elif Getter == 1:
                    try:
                        await TempClient.sign_in(phone=Number, code=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ Voip Added Correctly ✅**",
                                        buttons=[[Button.inline("🔙 back", "voip")]])
                    except SessionPasswordNeededError:
                        Getter = 2
                        await e.respond("**🔑 Insert the password (2FA) 🔑**",
                                        buttons=[[Button.inline("❌ Cancel", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ Wrong code ❌**", buttons=[[Button.inline("🔄 Try Again", "addvoip")]])
                elif Getter == 2:
                    try:
                        await TempClient.sign_in(phone=Number, password=e.text)
                        SSs[Number] = StringSession.save(TempClient.session)
                        Getter, Number = None, None
                        saveSS()
                        await e.respond("**✅ Voip Added Correctly ✅**",
                                        buttons=[[Button.inline("🔙 Back", "voip")]])
                    except:
                        Getter, Number = None, None
                        await e.respond("**❌ Wrong Password ❌**", buttons=[[Button.inline("🔄 Try Again", "addvoip")]])
                elif Getter == 3:
                    Getter = None
                    if e.text in SSs:
                        await e.respond(f"**🔧 Management »** `{e.text}`", buttons=[
                            [Button.inline("📁 Archive", "arch;" + e.text)],
                            [Button.inline("👁️ View", "visualizza;" + e.text),
                             Button.inline("🔧Change Info", "setta;" + e.text)], [
                                Button.inline("➖ Delete ", "del;" + e.text)], [Button.inline("🔙 Back", "voip")]])
                    else:
                        await e.respond("**❌ Voip Not Found ❌**", buttons=[[Button.inline("🔄 Try Again", "voips")]])
                elif Getter == 4:
                    Getter = None
                    if e.text in ArchSSs:
                        await e.respond(f"**🔧 Management »** `{e.text}`", buttons=[
                            [Button.inline("➕ Re-add", "add;" + e.text),
                             Button.inline("➖ Remove", "delarch;" + e.text)], [Button.inline("🔙 Back", "voip")]])
                    else:
                        await e.respond("**❌ Voip Not found ❌**", buttons=[[Button.inline("🔄 Try Again", "voips")]])
                elif Getter == 5:
                    Getter = None
                    if e.text != None and e.text != "":
                        if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
                            if not " " in e.text:
                                Grab = e.text
                                await e.respond("**✅ Group Set Correctly✅**",
                                                buttons=[[Button.inline("✔ Steal", "add")],
                                                         [Button.inline("🔙 Back", "grab")]])
                            else:
                                await e.respond("**❌ At the moment you can only enter one group ❌**",
                                                buttons=[[Button.inline("🔄 Try Again", "setgrab")]])
                        else:
                            await e.respond("**❌ You must enter a link or @ of a group ❌**",
                                            buttons=[[Button.inline("🔄 Try Again", "setgrab")]])
                    else:
                        await e.respond("**⚠️ Format Not Good ⚠️**",
                                        buttons=[[Button.inline("🔄 Try Again", "setgrab")]])
                elif Getter == 6:
                    Getter = None
                    skipped = 0
                    if e.text != None and e.text != "":
                        if "t.me/" in e.text or "telegram.me/" in e.text or e.text.startswith("@"):
                            if not " " in e.text:
                                inAdding = True
                                limitati = 0
                                banned = []
                                limited = []
                                Users = []
                                gruppo1_skipped =0
                                gruppo2_skipped = 0
                                countusers = 0
                                msg = await e.respond(
                                    "**✅ Added Members In Progress ✅**\nWait " + str(len(SSs) * 125) + " seconds (approximately)..",
                                    buttons=[[Button.inline("❌ Stop", "stop")]])
                                for SS in SSs:
                                    isAlive = False
                                    CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH)
                                    await CClient.connect()
                                    try:
                                        me = await CClient.get_me()
                                        if me == None:
                                            isAlive = False
                                        else:
                                            isAlive = True
                                    except:
                                        isAlive = False
                                    if isAlive:
                                        async with CClient as client:
                                            try:
                                                if "/joinchat/" in Grab:
                                                    if Grab.endswith("/"):
                                                        l = len(Grab) - 2
                                                        Grab = Grab[0:l]
                                                    st = Grab.split("/")
                                                    L = st.__len__() - 1
                                                    group = st[L]
                                                    try:
                                                        await client(ImportChatInviteRequest(group))
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        await client(JoinChannelRequest(Grab))
                                                    except:
                                                        pass
                                                ent = await client.get_entity(Grab)
                                                try:
                                                    users = client.iter_participants(ent.id, aggressive=True)
                                                    ent2 = await client.get_entity(e.text)
                                                    await asyncio.sleep(0.5)
                                                    users2 = client.iter_participants(ent2.id, aggressive=True)
                                                    Users2 = []
                                                    async for user2 in users2:
                                                        Users2.append(user2.id)

                                                    async for user in users:
                                                        try:
                                                            if not user.bot and not user.id in Users:
                                                                if not user.id in Users2:
                                                                    if activeusers:
                                                                        accept = True
                                                                        try:
                                                                            lastDate = user.status.was_online
                                                                            num_months = (
                                                                                                 datetime.now().year - lastDate.year) * 12 + (
                                                                                                 datetime.now().month - lastDate.month)
                                                                            if (num_months > 1):
                                                                                accept = False
                                                                        except:

                                                                            continue
                                                                        if accept:
                                                                            Users.append(user.id)
                                                                    else:
                                                                        Users.append(user.id)

                                                        except:
                                                            pass
                                                except FloodWaitError as err:
                                                    await msg.edit(
                                                        f"**⏳ Wait for more {err.seconds}, the current voip will be skipped. and I'll move on to the next voip after waiting ⏳**")
                                                    await asyncio.sleep(err.seconds + 4)
                                                    gruppo2_skipped = gruppo2_skipped + 1
                                                    skipped = skipped + 1
                                                    pass
                                            except FloodWaitError as err:
                                                await msg.edit(
                                                    f"**⏳ Wait for more {err.seconds}, the current voip will be skipped. and I'll move on to the next voip after waiting  ⏳**")
                                                await asyncio.sleep(err.seconds + 4)
                                                gruppo2_skipped = gruppo2_skipped + 1
                                                skipped = skipped + 1
                                                pass
                                            except:
                                                gruppo1_skipped = gruppo1_skipped+1
                                                skipped = skipped +1
                                                pass
                                            try:
                                                if "/joinchat/" in e.text:
                                                    if e.text.endswith("/"):
                                                        l = len(e.text) - 2
                                                        text = e.text[0:l]
                                                    else:
                                                        text = e.text
                                                    st = text.split("/")
                                                    L = st.__len__() - 1
                                                    group2 = st[L]
                                                    try:
                                                        await client(ImportChatInviteRequest(group2))
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        await client(JoinChannelRequest(e.text))
                                                    except:
                                                        pass
                                                gialimitato = False

                                                canAdd = True
                                                await asyncio.gather(addUsers(client, Users, ent2.id), timeoutAdd(120))
                                                spambotchat = await client.get_entity("spambot")
                                                await client.send_message(spambotchat, "/start")
                                                messaggiospambot = await client.get_messages(spambotchat, limit=1)
                                                try:
                                                    if "re free" in messaggiospambot[0].message or "Free" in \
                                                            messaggiospambot[0].message:
                                                        print("free")
                                                    else:
                                                        gialimitato = True
                                                        limitati = limitati + 1
                                                        limited.append(SS)
                                                        print("not free")
                                                        try:
                                                            start = messaggiospambot[0].message.index(
                                                                "account is now limited until ") + len(
                                                                "account is now limited until ")
                                                            end = messaggiospambot[0].message.index(", 16:38 UTC",
                                                                                                    start)
                                                            e = messaggiospambot[0].message[start:end]
                                                            date2 = datetime.strptime(e, '%d %b %Y')
                                                            date2 += timedelta(days=1)
                                                            raspingintelligentelist[SS] = date2

                                                        except ValueError:
                                                            print("error")
                                                except Exception as e5:
                                                    print(e5)



                                                if tentativi > countusers and not gialimitato:
                                                    date2 = (datetime.now() + timedelta(hours=6))
                                                    raspingintelligentelist[SS] = date2
                                                    limitati = limitati + 1
                                                    limited.append(SS)

                                                for user in AddedUsers:
                                                    if user in Users:
                                                        Users.remove(user)
                                            except FloodWaitError as err:
                                                await msg.edit(
                                                    f"**⏳ Wait for more {err.seconds}, the current voip will be skipped. and I'll move on to the next voip after waiting  ⏳**")
                                                await asyncio.sleep(err.seconds + 4)
                                                gruppo2_skipped = gruppo2_skipped + 1
                                                skipped = skipped + 1
                                                pass
                                            except:
                                                gruppo2_skipped = gruppo2_skipped + 1
                                                skipped = skipped +1
                                                pass
                                    else:
                                        banned.append(SS)
                                        await e.respond(
                                            f"**⚠️ WARNING »** __Il voip__ '{SS}' __Could being banned from telegram! If you only disconnected it by mistake re-add it ;)__")
                                if archivialimitati:
                                    if limited.__len__() > 0:
                                        for n2 in limited:
                                            if n2 in SSs:
                                                if not n2 in ArchSSs:
                                                    ArchSSs[n2] = SSs[n2]
                                                    saveArchSS()
                                                del (SSs[n2])
                                                saveSS()

                                if banned.__len__() > 0:
                                    for n in banned:
                                        if n in SSs:
                                            del (SSs[n])
                                    saveSS()
                                inAdding = False
                                if gruppo2_skipped > gruppo1_skipped:
                                    await msg.edit("**✅ Adding Members Completed ✅**" + "\nAdding: " + str(
                                        countusers) + "  ⏳⏳⏳  on a maximum of : " + str(
                                        maxusers) + "\n\n📱Voip skipped (try again, to try to make them all work.): " + str(
                                        skipped) + " su " + str(
                                        len(SSs) +limitati) + "\n♨️Limited Voip : " + str(limitati) + " on " + str(len(
                                        SSs) +limitati) + "\n\n🔬DIAGNOSIS: the biggest problem is on the second group.n🤗I would advise: private groups, or channels, are not compatible."+"\n Genius Adding is: " + str(archivialimitati),
                                                   buttons=[[Button.inline("🔙 Back", "back")]])
                                elif gruppo1_skipped > gruppo2_skipped:
                                    await msg.edit("**✅ Adding Members Completed ✅**" + "\nAggiunti: " + str(
                                        countusers) + "  ⏳⏳⏳  on a maximum of: " + str(
                                        maxusers) + "\n\n📱Voip skipped (try again, to try to make them all work.): " + str(
                                        skipped) + " su " + str(len(
                                        SSs) +limitati) + "\n♨️Limited Voip : " + str(limitati) + " su " + str(len(
                                        SSs) +limitati) + "\n\n🔬DIAGNOSIS: the biggest problem is on the second group.n🤗I would advise: private groups, or channels, are not compatible."+"\n Genius Adding is: " + str(archivialimitati),
                                                   buttons=[[Button.inline("🔙 Back", "back")]])
                                else:
                                    await msg.edit("**✅ Adding Members Completed ✅**" + "\nAdded: " + str(
                                        countusers) + "  ⏳⏳⏳  on a maximum of: " + str(
                                        maxusers) + "\n\n📱Voip skipped (try again, to try to make them all work.): " + str(
                                        skipped) + " su " + str(len(
                                        SSs) + limitati) + "\n♨️Limited Voip : " + str(limitati) + " su " + str(len(
                                        SSs) + limitati)+"\n Genius Adding🧠 is: " + str(archivialimitati), buttons=[[Button.inline("🔙 Back", "back")]])

                            else:
                                await e.respond("**❌ At the moment you can only enter one group ❌**",
                                                buttons=[[Button.inline("🔄 Try Again", "add")]])
                        else:
                            await e.respond("**❌ You must enter a link or @ of a group ❌**",
                                            buttons=[[Button.inline("🔄 Try Again", "add")]])
                    else:
                        await e.respond("**⚠️ Invalid Format ⚠️**", buttons=[[Button.inline("🔄 Try Again", "add")]])
                elif Getter == 9:
                    Getter = None
                    try:
                        await TempClient(UpdateUsernameRequest(e.text))
                        await e.respond("✅Username set✅",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                    except:
                        await e.respond("❌username invalid/available❌!\nusername not set!",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                elif Getter == 10:
                    Getter = None
                    try:
                        path = await bot.download_media(e.media)
                        print(path)
                        await TempClient(UploadProfilePhotoRequest(
                            await TempClient.upload_file(path)
                        ))
                        await e.respond("✅Pic Set✅",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                    except Exception as e:
                        print(str(e))
                        await e.respond("❌Pic not set❌!\nError in formato of photos!",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                elif Getter == 12:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            first_name=e.text
                        ))
                        await e.respond("✅Name set✅",
                                        buttons=[[Button.inline("🔙                                         SSs) +limitati) + "\n\n🔬DIAGNOSIS: the biggest problem is on the second group.n🤗I would advise: private groups, or channels, are not compatible."+"\n Genius Adding is: " + str(archivialimitati),
", "back")]])
                    except:
                        await e.respond("❌Name not set❌!\nError in insert name!",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                elif Getter == 13:
                    Getter = None
                    try:
                        await TempClient(UpdateProfileRequest(
                            last_name=e.text
                        ))
                        await e.respond("✅Surname Set✅",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                    except:
                        await e.respond("❌Surname not set ❌!\nError in insert Surname!",
                                        buttons=[[Button.inline("🔙 Back", "back")]])
                elif Getter == 19 and e.chat_id == ADMIN:
                    Getter = None
                    maxusers = int(e.text)
                    await e.respond("Users maximum set a: " + str(maxusers),
                                    buttons=[[Button.inline("🔙 Back", "back")]])

            else:
                text1 = e.text.split(" ")
                try:
                    if "/admin" in text1[0] and e.chat_id == ADMIN:
                        ADMINS.append(int(text1[1]))
                        await e.respond("Made Admin" + text1[1])
                    elif "/unadmin" in text1[0] and e.chat_id == ADMIN:
                        ADMINS.remove(int(text1[1]))
                        await e.respond("removed admin " + text1[1])
                except Exception as e4:
                    print(str(e4))


@bot.on(events.CallbackQuery())
async def callbackQuery(e):
    global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, Grab, inAdding, ADMINS, controllolimitato, activeusers, maxusers,archivialimitati,raspingintelligentelist
    if e.sender_id == ADMIN or e.sender_id in ADMINS:
        if e.data == b"back":
            Getter, Number, TempClient = None, None, None
            await e.edit("**🤖 Raspa Bot Panel \ n \ n⚙ Version »4.4 **", buttons = [[Button.inline ("📞 Voip", "voip")],
                                                                                    [Button.inline ("👥 Steal", "grab"),
                                                                                     Button.inline ("✔ Add", "add")], [
                                                                                        Button.inline (
                                                                                            "🎛️ADMIN PANEL",
                                                                                            "adminpanel")]])
        elif e.data == b"adminpanel":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control.", alert=True)
            else:
                await e.edit("choose an option:", buttons=[[Button.inline("max users📌", "maxutentiset")],
                                                           [Button.inline("active only", "activiset")],
                                                           [Button.inline("GET VOIP📳 FILE", "getSSS")],
                                                           [Button.inline("Genius ADDING🧠", "limitatiset")],
                                                           [Button.inline("RE-ADD SMART🧠", "readd")],
                                                           [Button.inline("LIMITED INFO🧠", "limitinfo")],
                                                           [Button.inline("🔙 Back", "back")]])
        elif e.data == b"maxutentiset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control.", alert=True)
            else:
                Getter = 19
                await e.edit("Insert a numer of Users:", buttons=[[Button.inline("🔙 Back", "back")]])
        elif e.data == b"readd":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control", alert=True)
            else:
                raspcontrollo =raspacontrol()
                await e.answer("HAVE ANY VOIP BEEN RE-ADDED? 🧠 is: " + str(raspcontrollo), alert=True)
        elif e.data == b"limitinfo":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control.", alert=True)
            else:
                for data4 in raspingintelligentelist:
                    await e.client.send_message(e.sender_id,
                                                "the voip" + data4 + "will be slimmed on:" + raspingintelligentelist[
                                                    data4].strftime('% d /% m /% Y% H:% M'))
                    await e.client.send_message(e.sender_id,
                                                "** INFO OBTAINED. \ n (if you did not get anything, you have no currently limited voips REGISTERED IN BOT) \n \n🤖 Raspa Bot panel \n \n⚙ Version» 4.4 ** ",
                                                buttons=[[Button.inline("📞 Voip", "voip")],
                                                         [Button.inline("👥 Steal", "grab"),
                                                          Button.inline("✔ Add", "add")],
                                                         [Button.inline("🎛️ADMIN PANEL", "adminpanel")]])
        elif e.data == b"limitatiset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control", alert=True)
            else:
                archivialimitati = not archivialimitati
                await e.answer("ADDING INTELLIGENTE🧠 is: " + str(archivialimitati), alert=True)
        elif e.data == b"attiviset":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control", alert=True)
            else:
                activeusers = not activeusers
                await e.answer("solo attivi is: " + str(activeusers), alert=True)

        elif e.data == b"getSSS":
            if controllolimitato and e.sender_id != ADMIN:
                await e.answer("you do not have the ability to access it .. \nlimit control", alert=True)
            else:
                await e.respond("here is the FILE Voip📳", file="SSs.json",buttons=[
                                                            [Button.inline("🔙 Back", "back")]])
        elif e.data == b"stop":
            await e.edit("**✅ Adding Cancel ✅**", buttons=[[Button.inline("🔙 Back", "back")]])
            python = sys.executable
            if controllolimitato:
                os.execl(python, python, *sys.argv, "Y")
            else:
                os.execl(python, python, *sys.argv, "N")
        elif inAdding:
            await e.answer("❌» This section is locked while adding members!", alert=True)
        elif e.data == b"voip":
            Getter, Number, TempClient = None, None, None
            await e.edit(f"__📞 Added Voip »__ **{SSs.__len__()}**",
                         buttons=[[Button.inline("➕ Add", "addvoip"), Button.inline("🔧 Management", "voips")],
                                  [Button.inline("📁 Archived", "arch")], [Button.inline("🔙 Back", "back")]])
        elif e.data == b"addvoip":
            Getter = 0
            await e.edit("**☎️ Enter the number of the voip you want to add ☎️**",
                         buttons=[Button.inline("❌ cancel", "voip")])
        elif e.data == b"voips":
            if SSs.__len__() > 0:
                Getter = 3
                msg = "__☎️ Invia il numero del voip che vuoi gestire__\n\n**LISTA VOIP**"
                for n in SSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ cancel", "voip")])
            else:
                await e.edit("**❌You have not added any voip ❌**",
                             buttons=[[Button.inline("➕ AddVoip", "addvoip")], [Button.inline("🔙 Back", "voip")]])
        elif e.data == b"arch":
            if ArchSSs.__len__() > 0:
                Getter = 4
                msg = f"__📁 Archived Voip »__ **{ArchSSs.__len__()}**\n\n__☎️ Send the number of the archived voip you want to manage__\n\n**List of Archived Voip**"
                for n in ArchSSs:
                    msg += f"\n`{n}`"
                await e.edit(msg, buttons=[Button.inline("❌ cancel", "voip")])
            else:
                await e.edit("**❌ You have not archived any voip ❌**", buttons=[[Button.inline("🔙 Back", "voip")]])
                elif e.data == b
                "grab":
                if Grab == None:
                    await e.edit("** ❌ Group Not Set ❌ \n \nℹ️ You can set it using the button below! **",
                                 buttons=[[Button.inline("✍🏻 Set", "setgrab")],
                                          [Button.inline("🔙 Back", "back")]])
                else:
                    await e.edit(f
                    "__ 👥 Group set» __ ** {Grab} ** ",
                    buttons = [[Button.inline("✍🏻 Edit", "setgrab")],
                               [Button.inline("🔙 Back", "back")]])
                    elif e.data == b
                    "setgrab":
                    Getter = 5
                    await e.edit("__ 👥 Send the @ or link of the group you want to steal users from! __",
                                 buttons=[Button.inline("❌ cancel", "back")])
                elif e.data == b
                "add":
                if SSs.__ len __ () > 0:
                    if Grab! = None:
                        Getter = 6
                        await e.edit("__ ➕ Send the @ or link of the group you want to add users to! __",
                                     buttons=[[Button.inline("❌ cancel", "back")]])
                    else:
                        await e.edit("** ❌ Set the group to steal users from ❌ **",
                                     buttons=[[Button.inline("👥 Steal", "grab")], [Button.inline("🔙 Back", "back")]])
                else:
                    await e.edit("** ❌ You haven't added any voip ❌ **",
                                 buttons=[[Button.inline("➕ Add", "addvoip")], [Button.inline("🔙 Back", "back")]])
        else:
            st = e.data.decode().split(";")
            if st[0] == "Setname":
                if st[1] in SSs:
                    Getter = 12
                    TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                    await TempClient.connect()
                    me = await TempClient.get_me()
                    await e.edit("** enter the name to enter for the account ** \ ncurrent name:" + me.first_name)
                    elif st[0] == "setsurname":
                    if st[1] in SSs:
                        Getter = 13
                        TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                        await TempClient.connect()
                        me = await TempClient.get_me()
                        await e.edit(
                            "** enter the surname to enter for the account ** \ ncurrent surname:" + str(me.last_name))
                elif st[0] == "getmsg":
                TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                await TempClient.connect()
                messages = await TempClient.get_messages(777000, limit=1)
                await e.client.send_message(e.sender_id,
                                            "your login message for voip is: \ n \ n" + messages[0].message)
                elif st[0] == "sect":
                if st[1] in SSs:
                    await e.edit(
                        "🔧VOIP SETTINGS🔧:" + st[1] + "\ nUse / start to return Back \ n \ nchoose what to do:",
                        buttons=[
                            [Button.inline("🔶GET MESSAGE🔶", "getmsg;" + st[1])],
                            [Button.inline("🔸SET USERNAME🔸", ​​"setusername;" + st[1])],
                    [Button.inline("🔹SET PROFILE PHOTO🔹", "setphoto;" + st[1])],
                    [Button.inline("🔶SET NAME🔶", "setname;" + st[1])],

                    [Button.inline("🔷SET SURNAME🔷", "setsurname;" + st[1])]])
                    elif st[0] == "show":
                    if st[1] in SSs:
                        try:
                            TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                            await TempClient.connect()
                            me = await TempClient.get_me()
                            path = await TempClient.download_profile_photo("me")
                            await bot.send_file(e.sender_id, path,
                                                caption="username:" + str(
                                                    me.username) + "\ nname:" + me.first_name + "\ nsurname:" + str(
                                                    me.last_name) + "\ nid:" + str(
                                                    me.id) + "\ nUSA / start to return Back",
                                                buttons=[[Button.inline("🔧VOIP SETTINGS🔧", "set;" + st[1])]])

                        except Exception as and:
                            print(str(e))
                elif st[0] == "setusername":
                    if st[1] in SSs:
                        Getter = 9
                        TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                        await TempClient.connect()
                        me = await TempClient.get_me()
                        await e.edit(
                            "** enter the username to enter for the account ** \ nusername current:" + me.username,
                            buttons=[[Button.inline("🔙 Back", "back")]])
                elif st[0] == "setphoto":
                    if st[1] in SSs:
                        Getter = 10
                        TempClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                        await TempClient.connect()
                        await e.edit("** send the photo to insert for the account **",
                                     buttons=[[Button.inline("🔙 Back", "voip")]])
                        elif st[0] == "arch":
                        if st[1] in SSs:
                            if not st[1] in ArchSSs:
                                ArchSSs[st[1]] = SSs[st[1]]
                                saveArchSS()
                            del (SSs[st[1]])
                            saveSS()
                            await e.edit("** ✅ Voip Filed Correctly ✅ **",
                                         buttons=[[Button.inline("🔙 Back", "voip")]])
                        else:
                            await e.edit("** ❌ Voip Not Found ❌ **", buttons=[[Button.inline("🔙 Back", "voip")]])
                    elif st[0] == "add":
                        if st[1] in ArchSSs:
                            SSs[st[1]] = ArchSSs[st[1]]
                            saveSS()
                            del (ArchSSs[st[1]])
                            saveArchSS()
                            await e.edit("** ✅ Voip Re-added Correctly ✅ **",
                                         buttons=[[Button.inline("🔙 Back", "voip")]])
                        else:
                            await e.edit("** ❌ Voip Not Found ❌ **", buttons=[[Button.inline("🔙 Back", "voip")]])
                    elif st[0] == "del":
                        if st[1] in SSs:
                            CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                            await CClient.connect()
                            try:
                                me = await CClient.get_me()
                                if me! = None:
                                    async with CClient as client:
                                        await client.log_out()
                            except:
                                pass
                            del (SSs[st[1]])
                            saveSS()
                            await e.edit("** ✅ Voip Removed Correctly ✅ **",
                                         buttons=[[Button.inline("🔙 Back", "voip")]])
                        else:
                            await e.edit("** ❌ Voip Already Removed ❌ **", buttons=[[Button.inline("🔙 Back", "voip")]])
                    elif st[0] == "delarch":
                        if st[1] in ArchSSs:
                            CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
                            await CClient.connect()
                            try:
                                me = await CClient.get_me()
                                if me! = None:
                                    async with CClient as client:
                                        await client.log_out()
                            except:
                                pass
                            del (ArchSSs[st[1]])
                            saveArchSS()
                            await e.edit("** ✅ Voip Removed Correctly ✅ **",
                                         buttons=[[Button.inline("🔙 Back", "voip")]])
                        else:
                            await e.edit("** ❌ Voip Already Removed ❌ **", buttons=[[Button.inline("🔙 Back", "voip")]])
                    elif st[0] == "info":
                        await e.answer(f
                        "ℹ️ The error occurred in the following voip» {st [1]} ℹ️ ")


                        print("please, insert the bot token ..")
                        bot.start()

                        bot.run_until_disconnected()