import click

@click.group(name="ip")
def ip_group():
    pass

@ip_group.group(name="route")
def ip_route():
    pass

@ip_route.command(name="add")
def ip_route_add():
    pass

@ip_route.command(name="del")
def ip_route_del():
    pass

@ip_route.command(name="list")
def ip_route_list():
    pass

@ip_group.group(name="nat")
def ip_nat():
    pass

@ip_nat.group(name="add")
def ip_nat_add():
    pass

@ip_nat_add.command(name="static")
def ip_nat_add_static():
    pass

@ip_nat_add.command(name="dynamic")
def ip_nat_add_dynamic():
    pass

@ip_nat.command(name="del")
def ip_nat_del():
    pass

if __name__ == "__main__":
    ip_group()
