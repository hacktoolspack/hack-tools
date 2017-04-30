# -*- coding: utf-8 -*-

from logging import log
import os

def email(to="nikisweeting+bot@gmail.com",subj='BOT',msg="Info",attch=[]): # function to send mail to a specified address with the given attachments
    # do not use attch.append() witin function http://stackoverflow.com/a/113198/2156113
    err = """\n
        sudo mkdir -p /Library/Server/Mail/Data/spool\n
        sudo /usr/sbin/postfix set-permissions\n
        sudo /usr/sbin/postfix start
        """
    if len(attch) > 0:
        for attachment in attch:
            try:
                cmd = 'uuencode %s %s | mailx -s "%s" %s' % (attachment.strip(), attachment.strip(), subj, to)
                log('[+] Sending email...')
                log('[<]    ',cmd)
                sts = run(cmd, public=False)
                return "Sending email to %s. (subject: %s, attachments: %s\n[X]: %s)" % (to, subj, str(attch), str(sts))
            except Exception as error:
                return str(error)
    else:
        p = os.popen("/usr/sbin/sendmail -t", "w")
        p.write("To: %s" % to)
        p.write("Subject: %s" % subj)
        p.write("\n") # blank line separating headers from body
        p.write('%s\n' % msg)
        sts = p.close()
    if sts != None:
        return "Error: %s. Please fix Postfix with: %s" % (sts, err)
    else:
        return "Sent email to %s. (subject: %s, attachments: %s)" % (to, subj, str(attch))