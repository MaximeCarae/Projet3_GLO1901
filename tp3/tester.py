from quoridor import Quoridor


partie = Quoridor(["rod", "jimbo"])
print(partie)

print(partie.placer_mur(1, [1, 8], "horizontal"))
print(partie)

try:
    partie.placer_mur(1, [2, 8], "horizontal")
except:
    print("aaaaaaaaaaaaaaaaaaaaa")
print(partie)

partie.placer_mur(1, [3, 8], "horizontal")
print(partie)

partie.placer_mur(1, [3, 4], "vertical")
print(partie)

try:
    partie.placer_mur(1, [3, 5], "vertical")
except:
    print(".awemc3eic43icm3ocmn3rkco ")

partie.placer_mur(1, [3, 6], "vertical")
partie.placer_mur(1, (2, 1), "qmce")

print(partie)
