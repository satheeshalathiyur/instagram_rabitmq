import json
from dxy.utils.instagram.client import InstagramAPI
from dxy.models.social.smh_instagram import InstagramCredential
from dxy import settings
from dxy.utils.instagram.bind import InstagramAPIError
from dxy.utils.mail import send_email
import logger
def instagram_fetch():
        user_id = None
        xml_feed = {}
        xml_feed["items"] = []
            
        client_secret = settings.INSTAGRAM_CLIENT_SECRET
            
        logger.debug('Fetching Instagram images %s...' % ic.url)
        try:
                inst_dtl_obj = InstagramCredential.objects.with_id(ic.inst_crdntl)
        except:
                inst_dtl_obj = None
                
        if inst_dtl_obj:
                api = InstagramAPI(access_token=inst_dtl_obj.access_token, client_secret=client_secret)
                try:
                    recent_media, next_ = api.user_recent_media(user_id=inst_dtl_obj.userid)
                except InstagramAPIError:
                    recent_media = None
                    ic.enabled = False
                    ic.save()
                    subject = '(Error), Instagram importing failed for site: %s' % ic.site.title
                    body = 'Import from Instagram Api failed for site %s, with import content id: %s\n\
                    Import configuration has been disabled. Enable it after fixing error from site settings' % (ic.site.title, ic.id)
                    body += " Error is due to:"+str(InstagramAPIError)
                    send_email(subject, body, 'devsad@iprsoftware.com')

                except:
                    recent_media = None
                list_data = []
                if recent_media:
                    for media in recent_media:
                        items = {}
                        items['id'] = media.id
                        if media.caption:
                            items['title'] = media.caption.text[:90] + '...'
                            items['summary'] = media.caption.text
                        else:
                            items['title'] = "instagram image of %s" % str(media.user.full_name)
                        items['link'] = media.link
                        items['author'] = media.user.username
                        items['published'] = str(media.created_time)
                        list_data.append(items)
                else:
                    logger.debug('recent media ERROR')
                xml_feed["items"] = list_data 
        else:
            logger.debug('Fetching XML feed from %s...' % ic.url)
            try:
                xml_feed = feedparser.parse(ic.url)
            except ImportError:
                logger.exception('Failed to Parse XML')

if __name__=="__main__":
    instagram_fetch()
        