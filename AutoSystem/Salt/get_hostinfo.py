if __name__ == "__main__":
    import os,sys,django
    BASE_DIR = os.path.dirname(os.getcwd())
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'AutoSystem.settings'
    django.setup()

from Salt.SaltAPI import *
from Assets.models import *
from Salt.models import *
from django.utils import timezone

class get_hostinfo:
    def __init__(self,area):
        self.area = area
        self.gid = group.objects.get(group_name='UNKNOW')
        self.area_id = Area.objects.get(area_name=area)
        try:
            Area.objects.get(area_name=self.area)
            api_info = Salt_info.objects.get(Area_name=area)
            self.salt = Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
        except Exception,e:
            print e
    def update_host(self,host):
        if Host.objects.filter(salt_key_name = host).exists() == False:
            info = self.salt.Salt_Minions(host)
            if len(info['return'][0]) == 1:
                try:
                    nip1 = info['return'][0][host]['ip4_interfaces']['eth0'][0]
                    hostname = info['return'][0][host]['fqdn']
                except KeyError:
                    print 'KeyError'
                if Host.objects.filter(host_nip = nip1).exists() == False:
                    host=Host(host_name=hostname,host_nip=nip1,group_id=self.gid,area=self.area_id,salt_key_name=host,host_status='Active')
                    host.save()
                print hostname
    def update_area_host(self):
        minions,minions_pre = self.salt.ListKey()
        for host in minions:
            print "+++++++++"+host
            self.update_host(host)

    def update_host_info(self,salt_key_name):
        print salt_key_name
        common_info = self.salt.Salt_Minions(salt_key_name)
        if len(common_info['return'][0]) == 1:
            disk_info = self.salt.Salt_CMD(salt_key_name,'disk.usage')
            mem_info = self.salt.Salt_CMD(salt_key_name,'status.meminfo')
            hostname = common_info['return'][0][salt_key_name]['fqdn']
            cpu_model = common_info['return'][0][salt_key_name]['cpu_model']
            cpu_num = common_info['return'][0][salt_key_name]['num_cpus']
            ip = common_info['return'][0][salt_key_name]['ip4_interfaces']['eth0'][0]
            pmem = mem_info['return'][0][salt_key_name]['MemTotal']['value']
            vmem = mem_info['return'][0][salt_key_name]['SwapTotal']['value']
            os = common_info['return'][0][salt_key_name]['os']
            disk_total = disk_info['return'][0][salt_key_name]['/']['1K-blocks']
            kernel_version = common_info['return'][0][salt_key_name]['kernelrelease']
            print ip
            if servers_info.objects.filter(host_ip=ip).exists():
                pass
            else:
                server_info=servers_info(host_name=hostname,
                                        host_ip=Host.objects.get(host_nip=ip),
                                        p_mem = pmem,
                                        v_mem = vmem,
                                        cpu_models = cpu_model,
                                        cpu_count = cpu_num,
                                        system_type = os,
                                        disk_total = disk_total,
                                        kernel_version = kernel_version,
                                        update_time = timezone.now())
                server_info.save()


if __name__ == "__main__":
    hostinfo=get_hostinfo(sys.argv[1])
    #hostinfo.update_area_host()
    for host in Host.objects.all():
        #print host.salt_key_name
        hostinfo.update_host_info(host.salt_key_name)

