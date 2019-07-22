# Dinoroar

Scripts, configuration and documentation for rebuilding the STEMosaur as a 
snips.ai satellite with a Raspberry Pi Zero W, sound card and battery.

# Why rebuild the STEMosaur?

Because the kiddo loved it and was heartbroken when it stopped working. It's
pretty crap that the company that built it didn't so much as send an email
to let people know that they were going out of business, leaving all of us
that bought it with a hunk of useless plastic.

And also because it seemed like a fun project. Because this is all going to be
built on open-source tools, I can keep tweaking and improving it, and eventually
it might be a project that I get to work on with my kid instead of for her.

# Why is it called Dinoroar?

That was the name the kiddo gave to her STEMosaur. She loves Peppa Pig, what can
I say?

# What will Dinoroar be able to do?

We mostly used him to tell bedtime stories, so that's first on the list. After
that, I'll probably work on streaming music. Interactive games/exercises may
come later, depending on time and interest.

# What do I need to rebuild the STEMosaur?

For my STEMosaur, I used the following (YMMV):

 * Raspberry Pi Zero W; it's small and has built-in WiFi and Bluetooth
 * Raspiaudio Mic+; there's no soldering required, and it has a detachable microphone if needed
 * Pisugar battery module; I was able to find a good sale, so I opted for the 1200mAh
 * Some sort of rubber padding to keep everything in place; I used self-adhesive anti-skid furniture pads because they were easy to work with
 * A Raspberry Pi 3/4, or other computer to use as the base station; The Raspberry Pi Zero isn't powerful enough to run the full snips audio server, so it will need to be tethered to something more substantial.

You'll also need a tool to cut up your STEMosaur so that everything will fit
inside, and so that you can connect a power cable to the battery module. I also
cut holes for the Mini HDMI connection, microUSB port and audio out, but that's
not strictly necessary. I recommend using a Dremel with a plastic cutting blade
for the large cuts, and then a smaller bit or even a drill to make the cuts for
the ports.

