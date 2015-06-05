import models_accounts as ma
import models_purchase as mp
import models_items as mi

ma.init_db()
indx = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
for i in indx:
	a = ma.Account('User' + str(i), 'qwerty' + str(i))
	ma.db_session.add(a)
ma.db_session.commit()

mp.init_db()

mi.init_db()

mi.db_session.add(mi.Item('Sword of power', 2023, params='Damage:10,Speed:1.2,Damage per. sec.:8.3'))
mi.db_session.add(mi.Item('Staff of fire', 1842, params='Damage:18,Speed:2.1,Damage per. sec.:8.6'))
mi.db_session.add(mi.Item('Book of wisdom', 3619, params='Intellect:2,Mana:20,Spirit:4'))
mi.db_session.add(mi.Item('Leather chest', 4781, params='Defense:18,Stamina:2,Agility:4'))
mi.db_session.add(mi.Item('Leather boots', 4923, params='Defense:12,Stamina:1,Agility:2'))
mi.db_session.add(mi.Item('Leather gloves', 1255, params='Defense:8,Agility:2'))
mi.db_session.add(mi.Item('Leather belt', 1724, params='Defense:2,Agility:1'))
mi.db_session.add(mi.Item('Leather pants', 1284, params='Defense:26,Stamina:6,Agility:8'))

mi.db_session.commit()