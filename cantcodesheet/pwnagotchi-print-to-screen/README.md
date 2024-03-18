# pwnagotchi-print-to-screen
Sample code to show how to use a plugin to print directly to a Pwnagotchi screen.


__Credit goes to:__  ```hannadiamond```

https://github.com/hannadiamond/pwnagotchi-plugins

It was their code that allowed me to figure out how to print text directly to the pwnagotchi screen (as a label) and to the view area.

# Setup

1) Copy over ```printp.py``` into your custom plugins directory.

2) In your ```config.toml``` file add:

```ruby

main.plugins.printp.enabled = true
main.plugins.printp.t0_x_coord = 0
main.plugins.printp.t0_y_coord = 13  #places T0 label right above the name of pwnagotchi
main.plugins.printp.tn_x_coord = 65  #places Tn label adjacent/to the right of T0 label 
main.plugins.printp.tn_y_coord = 13  #places Tn label right above the name of pwnagotchi

```

3) Restart your device to see your new timestamps and sample text!
