import discord



Dungeon = 'https://cdn.discordapp.com/attachments/1032198460767744064/1041280191122640976/image.png'
Village = 'https://cdn.discordapp.com/attachments/1032198460767744064/1046372443641610361/image.png'
Forest = 'https://cdn.discordapp.com/attachments/1032198460767744064/1058610024500428830/image.png'
River = 'https://cdn.discordapp.com/attachments/1032198460767744064/1058611426861797476/image.png'


Location3 = discord.Embed(title='Travelling...', colour=0xe67e22)
Location3.set_image(url=Dungeon)
Location3.add_field(name='Location:', value='You travelled to a Dungeon.')
Location3.add_field(name='Cmd available:', value='fight')
Location3.add_field(name='Danger meter:', value='High ⚠')

Location1 = discord.Embed(title='Travelling...', colour=0xe67e22)
Location1.set_image(url=Village)
Location1.add_field(name='Location:', value='You travelled to a village.')
Location1.add_field(name='Cmd available:', value='trade, shop.')
Location1.add_field(name='Danger meter:', value='Low ✅')

Location2 = discord.Embed(title='Travelling...', colour=0xe67e22)
Location2.set_image(url=Forest)
Location2.add_field(name='Location:', value='You travelled to a forest.')
Location2.add_field(name='Cmd available:', value=',search')
Location2.add_field(name='Danger meter:', value='Medium')

Location4 = discord.Embed(title='Travelling...', colour=0xe67e22)
Location4.set_image(url=River)
Location4.add_field(name='Location:', value='You travelled to a river.')
Location4.add_field(name='Cmd available:', value=',fish')
Location4.add_field(name='Danger meter:', value='Medium')


mainlocation = [{"x":151,"y":72,"embed":Location1},
                {"x":32,"y":125,"embed":Location3},
                {"x":200,"y":21,"embed":Location2},
                {"x":252,"y":59,"embed":Location4},
                ]