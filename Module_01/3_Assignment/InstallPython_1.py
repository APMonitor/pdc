module='gekko'
try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain
pipmain(['install',module])