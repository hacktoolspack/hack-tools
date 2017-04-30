#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# author: Liar.Bing 
# description: 获取腾讯企业邮箱通讯录 

import requests 
import re 

import sys; 
reload(sys); 

sys.setdefaultencoding('utf8'); 



def print_tree(id, department_infos, level, staff_infors, f): 
  prefix = '----' * level 
  text = prefix + department_infos[id]['name'] + prefix 
  print text 
  f.write(text + '\n') 
  for key, value in department_infos.items(): 
    if value['pid'] == id: 
       
      print_tree(value['id'], department_infos, level+1, staff_infors, f) 
  prefix = '    ' * level   
  for staff in staff_infors: 
    if staff['pid'] == id: 
      text = prefix + staff['name'] + '  ' + staff['alias'] 
      print text 
      f.write(text + '\n') 

if __name__ == "__main__": 
  # url参数中的sid 
  sid = '' 
  # cookie中的qm_sid 和 qm_username 
  qm_sid = '' 
  qm_username='' 

  all_departments_url = 'http://exmail.qq.com/cgi-bin/laddr_biz?action=show_party_list&sid={sid}&t=contact&view=biz'.format(sid=sid) 
  cookies = dict(qm_sid=qm_sid 
    , qm_username=qm_username) 
  request = requests.get(all_departments_url,cookies=cookies) 

  text = request.text 
  regexp = r'{id:"(\S*?)", pid:"(\S*?)", name:"(\S*?)", order:"(\S*?)"}' 
  results = re.findall(regexp, text) 
  department_ids = [] 
  department_infors = dict() 
  root_department = None 
  for item in results: 
     
    department_ids.append(item[0]) 
    department = dict(id=item[0], pid=item[1], name=item[2], order=item[3]) 
     
    department_infors[item[0]] = department 
    if item[1] == 0 or item[1] == '0': 
      root_department = department 

  regexp = r'{uin:"(\S*?)",pid:"(\S*?)",name:"(\S*?)",alias:"(\S*?)",sex:"(\S*?)",pos:"(\S*?)",tel:"(\S*?)",birth:"(\S*?)",slave_alias:"(\S*?)",department:"(\S*?)",mobile:"(\S*?)"}' 
  limit = 10000 

  all_emails = [] 
  staff_infors = [] 
  for department_id in  department_ids: 
    department_staff_url = 'http://exmail.qq.com/cgi-bin/laddr_biz?t=memtree&limit={limit}&partyid={partyid}&action=show_party&sid={sid}'.format(limit=limit, sid=sid, partyid=department_id) 
     
    request = requests.get(department_staff_url,cookies=cookies) 
     
    text = request.text 
     
    results = re.findall(regexp, text) 

     
    for item in results: 
      all_emails.append(item[3]) 
       
      staff = dict(uin=item[0], pid=item[1], name=item[2], alias=item[3], sex=item[4], pos=item[5], tel=item[6], birth=item[7], slave_alias=item[8], department=item[9], mobile=item[10]) 
      staff_infors.append(staff) 

  print str(len(all_emails)) + ' emails' 
  with open('all_emails.txt', 'w') as f: 
    for item in all_emails: 
      f.write(item + '\n') 
   
  with open('depart_staff_tree.txt', 'w') as f: 
    print_tree(root_department['id'], department_infors, 0, staff_infors, f)




#需要先手动登陆腾讯企业邮箱，然后把url中的sid(不是cookie里的)和cookie里的qm_sid、qm_username填到脚本里去，然后运行
