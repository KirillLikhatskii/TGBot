
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
import codecs

bot = Bot(token='Ваш токен')  # Объект бота
dp = Dispatcher()  # Диспетчер

@dp.message(CommandStart())
async def cmd_start(message: types.message):
    await message.answer('Приветсвую, больной, вижу тебе нужна запись к врачу, я к твоим услугам, список команд можно узнать при помощи команды /help')

@dp.message(Command('help'))
async def cmd_help(message: types.message):
    await message.answer('/zapis - записаться на приём\n Форма записи /zapis Ф И О Врач Время \n НЕ ЗАБЫВАЙТЕ СТАВИТЬ ПРОБЕЛЫ'
                         '/moizapisi ID(вашей записи) - просмотр созданных записей\n'
                         '/rmzapis ID Ф И О - отмена записи\n'
                         '/spisokvrach - список врачей')
@dp.message(Command('zapis'))
async def cmd_zapis(message: types.message):
    data = message.text[7: len(message.text)]
    next_step = False
    info = str(data).split(' ')
    file = codecs.open('spisok.txt', 'r', 'utf-8')
    spisok = file.read().split('\n')
    file.close()
    for i in range(0, len(spisok)):
        line = spisok[i].split(' ')
        if line[0] == info[3]:
            for j in range (1, len(line)):
                if line[j] == info[4]:
                    line[j] = 'ЗАНЯТО'
                    next_step = True
        spisok[i] = ' '.join(line)
    file = codecs.open('spisok.txt', 'w', 'utf-8')
    file.write('\n'.join(spisok))
    file.close()
    if next_step:
        counter = 0
        ID = 1
        for letter in data:
            if letter == ' ':
                counter+=1
        if counter == 4:
            file = codecs.open('zapisi.txt', 'r', 'utf-8')
            zapisi = file.read().split('\n')
            file.close()
            if len(zapisi)< 2:
                file = codecs.open('zapisi.txt', 'w', 'utf-8')
                file.write('{} {}\n'.format(ID, data))
                file.close()
                await message.answer('Запись успешно сформирована, ID вашей записи [{}]'.format(ID))
            else:
                numbers = []
                for j in range(0, len(zapisi)):
                    text = zapisi[j].split(' ')
                    if  (text[0] not in numbers):
                        numbers.append(text[0])
                    while str(ID) in numbers:
                        ID+=1
                file = codecs.open('zapisi.txt', 'a', 'utf-8')
                file.write('{} {}\n'.format(ID, data))
                file.close()
                await message.answer('Запись успешно сформирована, ID вашей записи [{}]'.format(ID))
        else:
            await message.answer('Некорректный ввод данных')
    else:
        await message.answer('Врач или время не найдено, либо ввод некорректен')
@dp.message(Command('moizapisi'))
async def cmd_moizap(message: types.message):
    data = message.text[11: len(message.text)]
    file = codecs.open('zapisi.txt', 'r', 'utf-8')
    zapisi = file.read().split('\n')
    file.close()
    for j in range(0, len(zapisi)):
        text = zapisi[j].split(' ')
        if data == text[0]:
            await message.answer('[ID] = {}\n[ФИО] = {} {} {}\n[Врач] = {}\n[Время] = {}'.format(text[0], text[1], text[2], text[3], text[4], text[5]))

@dp.message(Command('rmzapis'))
async def cmd_rmzap(message: types.message):
    data = message.text[9: len(message.text)]
    data = str(data).split(' ')
    file = codecs.open('zapisi.txt', 'r', 'utf-8')
    zapisi = file.read().split('\n')
    file.close()
    zapis = False
    for j in range(0,len(zapisi)):
        text = zapisi[j].split(' ')
        if data[0] == text[0]:
            if (text[1] == data[1]) and (text[2] == data[2]) and (text[3] == data[3]):
                file = codecs.open('spisok.txt', 'r', 'utf-8')
                spisok = file.read().split('\n')
                file.close()
                for i in range(0, len(spisok)):
                    line = spisok[i].split(' ')
                    if line[0] == text[4]:
                        for l in range(1, len(line)):
                            if line[l] == 'ЗАНЯТО':
                                line[l] = text[5]
                                spisok[i] = ' '.join(line)
                                break
                file = codecs.open('spisok.txt', 'w', 'utf-8')
                file.write('\n'.join(spisok))
                file.close()
                text[0]=text[1]=text[2]=text[3]=text[4]=text[5]=''
                zapisi[j] = ' '.join(text)
                file = codecs.open('zapisi.txt', 'w', 'utf-8')
                file.write('\n'.join(zapisi))
                file.close()
                zapis = True
            else:
                break
    if zapis:
        await message.answer('Запись успешно отменена')
    else:
        await message.answer('Записи с таким ID не существует, либо вы некорректно ввели ФИО')

@dp.message(Command('spisokvrach'))
async def cmd_sv(message: types.message):
    file = codecs.open('spisok.txt', 'r', 'utf-8')
    spisok = file.read()
    file.close()
    await message.answer(spisok)

async def Bot1():
    await dp.start_polling(bot)
