
class BiometricField(models.Model):
    def init(self, *args, **kwargs):
kwargs[‘max_length’] = 1000
super().init(*args, **kwargs)
def db_type(self, connection):
return ‘binary’