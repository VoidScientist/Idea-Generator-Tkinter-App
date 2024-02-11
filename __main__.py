import glob
import os
import tkinter as tk
import tkinter.ttk
from enum import Enum, auto
from Character import Character
from PropertyStorage import PropertyStorage


# states
class Menus(Enum):
    WELCOME = auto()
    GENERATE = auto()
    LOAD = auto()
    EDIT = auto()
    CONTENT = auto()


class EditMenus(Enum):
    EDITVALUES = auto()
    EDITKEYS = auto()

# global widgets
canvas: tk.Canvas
root: tk.Tk
menuFrame: tk.Frame
credit: tk.Label

# needed ressources
nextButton: tk.PhotoImage

# property storage on startup
loadedStor: PropertyStorage = PropertyStorage()

# window startup menu
openMenu = Menus.WELCOME
openEditMenu = EditMenus.EDITVALUES

# software version
version = "0.4a"

# window characteristics
wHeight = 750
wWidth = 1000

# TODO, when settings available, choose between modes, or just custom (only if there are users).
# colors variable
colorMode = "dark"
if colorMode == "dark":
    mainColor = "#2D3142"
    secondColor = "#4F5D75"
    highlightColor = "#6D7E9C"
elif colorMode == "light":
    mainColor = "#E7CFBC"
    secondColor = "#FFF4EC"
    highlightColor = "#FFFFFF"

# font variable
fontType = "Helvetica"
fontSizeBig = 20
fontSizeMedium = 18
fontSizeSmall = 10
fontSizeTiny = 8


# ======================================================================================================

def clearComponents(target, *exceptions):
    target.update()
    for child in target.winfo_children():
        if not child.winfo_name() in exceptions:
            child.destroy()


# ======================================================================================================

def childNum(widget: tk.Widget):
    widget.update()
    return len(widget.winfo_children())


# ======================================================================================================

def highlightButton(widget: tk.Widget, name: str):
    widget.update()
    for child in widget.winfo_children():
        if child.winfo_name() == name:
            child.configure(bg=highlightColor)
        else:
            child.configure(bg=secondColor)


# ======================================================================================================

def fitAllChilds(widget: tk.Widget):
    # placing menus
    for child in widget.winfo_children():
        index = widget.winfo_children().index(child)
        widgNum = childNum(widget)
        child.grid(row=0, column=index)
        child.place(relx=index / widgNum, relwidth=1 / widgNum, relheight=1)


# ======================================================================================================

def menuBar():
    global menuFrame, credit

    # frame for menu navigation
    menuFrame = tk.Frame(root, bd=5, relief="groove")

    # menu navigation buttons
    generate = tk.Button(menuFrame, text="Générer", font=(fontType, fontSizeBig), bg=secondColor,
                         command=lambda: changeMenu(Menus.GENERATE), name="generate")
    loadPropertyStorage = tk.Button(menuFrame, text="Charger propriétés", font=(fontType, fontSizeBig),
                                    bg=secondColor,
                                    command=lambda: changeMenu(Menus.LOAD), name="load")
    editPropertyStorage = tk.Button(menuFrame, text="Modifier propriétés", font=(fontType, fontSizeBig),
                                    bg=secondColor,
                                    command=lambda: changeMenu(Menus.EDIT), name="edit")
    content = tk.Button(menuFrame, font=(fontType, fontSizeBig), bg=secondColor,
                        text="Voir Contenu", name="contentMenu",
                        command=lambda: changeMenu(Menus.CONTENT))

    fitAllChilds(menuFrame)

    # placing the frame
    menuFrame.place(relheight=0.1, relwidth=1 - 4 / wWidth, relx=2 / wWidth)

    bottomFrame = tk.Frame(root, bg=secondColor, borderwidth=2, relief="groove")
    bottomFrame.place(rely=0.95, relwidth=1 - 4 / wWidth, relheight=0.05, relx=2 / wWidth)

    credit = tk.Label(bottomFrame, font=(fontType, fontSizeTiny), bg=secondColor,
                      text=f"Codé par VoidScientist || Version {version} -> Février 2022"
                           f" || Profil ouvert : {loadedStor.getName()}")
    credit.place(relheight=0.8, rely=0.5, anchor="w")


# ======================================================================================================

def changeMenu(openMenu):
    # shows active menu
    match openMenu:

        # ======================================================================================================

        case Menus.WELCOME:
            welcomeMessage = tk.Label(canvas, text="Bonsoir chers utilisateurs x)\n"
                                                   "Cette appli sert à générer des caractéristiques pour persos aléatoirement.\n\n"
                                                   "M'enfin, n'hésitez pas à me faire des retours sur l'interface ou l'appli en elle-même,\n"
                                                   "c'est la première que je crée, et je suis horrible en création d'interfaces xD\n"
                                                   "J'espère quand même que cette appli vous sera utile :)\n\n"
                                                   "- VoidScientist", font=(fontType, fontSizeMedium), bg=mainColor) \
                .place(rely=0.4, relx=0.5, anchor="center")

        case Menus.GENERATE:
            highlightButton(menuFrame, "generate")

            # generate and show a character
            def generateChar(stor: PropertyStorage, name: str = "Personnage"):
                if name == "":
                    name = "Personnage"
                characterDesc = tk.Text(canvas, bg=secondColor, font=(fontType, fontSizeMedium), width=35, height=10,
                                        borderwidth=2, relief="sunken")
                characterDesc.insert("end", Character(loadedStor.getData(), name=name).toStr())
                characterDesc.configure(state="disabled")
                characterDesc.place(relx=0.4, rely=0.4, anchor="center")

            clearComponents(canvas)

            characterName = tk.Entry(canvas, bg=secondColor, font=(fontType, fontSizeMedium), justify="center")
            characterName.place(rely=0.15, relx=0.4, anchor="center")

            charNameLabel = tk.Label(canvas, bg=mainColor, font=(fontType, fontSizeMedium), text="Nom :")
            charNameLabel.place(rely=0.15, relx=0.2, anchor="center")

            # on click, regenerate a character
            regenerate = tk.Button(canvas, image=nextButton,
                                   command=lambda: generateChar(loadedStor.getData(), characterName.get()))
            regenerate.place(relx=0.90, rely=0.4,
                             anchor="center")

            generateChar(loadedStor.getData(), "Personnage")

            # TODO add the command for the button
            copyToClipboard = tk.Button(canvas, text="Copier dans le presse papier", font=(fontType, fontSizeMedium),
                                        bg= secondColor)
            copyToClipboard.place(rely=0.65, relx=0.465, anchor="center")

            # TODO multiple caracteristics (if reaaaally needed)

        # ======================================================================================================

        case Menus.LOAD:
            highlightButton(menuFrame, "load")
            # create the label for the loaded stor
            actualLoadedStor: tk.Label
            keysText = "Entrez caractéristiques dispos (vide = défault) [ex: nation, race...]"

            #TODO rename system

            def getSaveFiles():
                res = []

                for files in glob.glob("saves\*.data"):
                    files = files.removeprefix("saves\\")
                    files = files.removesuffix(".data")
                    res.append(files)
                return res

            def deleteStor(lb: tk.Listbox):
                for i in lb.curselection():
                    name = lb.get(i)
                path = PropertyStorage(name=name).filepath
                os.remove(path)
                updateFileList()

            def updateFileList():
                fileList.delete(0, "end")
                for files in getSaveFiles():
                    fileList.insert("end", files)

            def createStor(name, keys: str = None):
                global loadedStor
                files = getSaveFiles()

                if name in files:
                    print("Name already exists!")
                    return

                if keys is not None and keys != keysText:
                    keys = keys.split(",")
                    for i in keys:
                        keys[keys.index(i)] = i.rstrip(" ").lstrip(" ")
                elif keys == keysText:
                    keys = None

                loadedStor = PropertyStorage(name, *keys)
                fileList.insert("end", loadedStor.name)

            def selectedItems(lb: tk.Listbox):
                global loadedStor

                for i in lb.curselection():
                    loadedStor = PropertyStorage(name=lb.get(i))
                    credit.configure(text=f"Codé par VoidScientist || Version {version} -> Février 2024"
                                          f" || Profil ouvert : {loadedStor.getName()}")

                actualLoadedStor.configure(text=f"'{loadedStor.getName()}' chargé.")

            clearComponents(canvas)

            fileList: tk.Listbox = tk.Listbox(canvas, font=(fontType, fontSizeMedium), justify="center",
                                              activestyle="underline", bg=secondColor)

            updateFileList()

            fileList.place(rely=0.3, relx=0.5, relwidth=0.2, relheight=0.2, anchor="center")

            changeLoadedStor = tk.Button(canvas, text="Charger", font=(fontType, fontSizeMedium), bg=secondColor,
                                         command=lambda: selectedItems(fileList))
            changeLoadedStor.place(relx=0.43, rely=0.45, anchor="center")

            deleteSelectedStor = tk.Button(canvas, text="Supprimer", font=(fontType, fontSizeMedium), bg=secondColor,
                                           command=lambda: deleteStor(fileList))
            deleteSelectedStor.place(relx=0.57, rely=0.45, anchor="center")

            actualLoadedStor = tk.Label(canvas, text=f"'{loadedStor.getName()}' chargé.",
                                        font=(fontType, fontSizeMedium),
                                        bg=secondColor, borderwidth=2, relief="ridge")
            actualLoadedStor.place(rely=0.1, relx=0.5, anchor="center")

            storName = tk.Entry(canvas, font=(fontType, fontSizeMedium - 1), bg=secondColor, justify="center", width=50)
            storName.place(rely=0.55, relx=0.5, anchor="center")
            storName.insert(0, "Entrez un nom de fichier")
            storName.bind("<FocusIn>",
                          lambda args: storName.delete(0, "end") if storName.get() == 'Entrez un nom de fichier'
                          else print(""))
            storName.bind("<FocusOut>",
                          lambda args: storName.insert(0, 'Entrez un nom de fichier') if storName.get() == ""
                          else print(""))

            storKeys = tk.Entry(canvas, font=(fontType, fontSizeMedium - 1), justify="center", bg=secondColor, width=50)
            storKeys.place(rely=0.6, relx=0.5, anchor="center")
            storKeys.insert(0, keysText)
            storKeys.bind("<FocusIn>", lambda args: storKeys.delete(0, "end"))

            storCreate = tk.Button(canvas, font=(fontType, fontSizeMedium), text="Créer", bg=secondColor,
                                   command=lambda: createStor(storName.get(),
                                                              storKeys.get()) if storName.get() != "" else print(""))
            storCreate.place(rely=0.66, relx=0.5, anchor="center")

        # ======================================================================================================

        case Menus.EDIT:
            highlightButton(menuFrame, "edit")

            # ======================================================================================================

            def editValuesMenu():
                highlightButton(editMenuFrame, "editValues")

                clearComponents(canvas, "editMenuBar")

                valueLabel = tk.Label(canvas, bg=mainColor, text="Valeurs :", font=(fontType, fontSizeMedium))
                valueLabel.place(rely=0.3, relx=0.35, anchor="e")

                values = tk.Entry(canvas, font=(fontType, fontSizeMedium), justify="center")
                values.insert(0, 'Exemple: val1,val2,val3')
                values.bind("<FocusIn>",
                            lambda args: values.delete(0,
                                                       "end") if values.get() == 'Exemple: val1,val2,val3' else print(
                                ""))
                values.bind("<FocusOut>",
                            lambda args: values.insert(0,
                                                       'Exemple: val1,val2,val3') if values.get() == "" else print(""))
                values.place(relx=0.5, rely=0.3, anchor="center")

                keyLabel = tk.Label(canvas, bg=mainColor, text="Clé :", font=(fontType, fontSizeMedium))
                keyLabel.place(rely=0.4, relx=0.35, anchor="e")

                keys = tk.ttk.Combobox(canvas, values=loadedStor.allowedKeys, font=(fontType, fontSizeMedium),
                                       justify="center")
                keys.place(relx=0.5, rely=0.4, anchor="center")

                actionsLabel = tk.Label(canvas, bg=mainColor, text="Action :", font=(fontType, fontSizeMedium))
                actionsLabel.place(rely=0.5, relx=0.35, anchor="e")

                actions = tk.ttk.Combobox(canvas, values=["Supprimer", "Ajouter"],
                                          font=(fontType, fontSizeMedium),
                                          justify="center")
                actions.place(relx=0.5, rely=0.5, anchor="center")

                def interpret():
                    action: str
                    if actions.get() == "Ajouter":
                        action = 'add'
                    elif actions.get() == "Supprimer":
                        action = "remove"
                    else:
                        print("Be sure to chose an action!")
                        return
                    loadedStor.userInterpret(values.get() + ":" + keys.get() + "&" + action)

                execute = tk.Button(canvas, text="Exécuter", font=(fontType, fontSizeMedium), command=interpret,
                                    bg=secondColor)
                execute.place(rely=0.6, relx=0.5, anchor="center")

            # ======================================================================================================

            def editKeysMenu():
                highlightButton(editMenuFrame, "editKeys")

                def updateKeyView():

                    viewKeys = tk.Text(canvas, bg=mainColor, font=(fontType, fontSizeMedium), width=18, height=8,
                                        bd=2, relief="sunken",background=secondColor)
                    viewKeys.insert("end", loadedStor.getKeys())
                    viewKeys.configure(state="disabled")
                    viewKeys.place(rely=0.4, relx=0.8, anchor="center")

                clearComponents(canvas, "editMenuBar")

                keyLabel = tk.Label(canvas, bg=mainColor, text="Clé :", font=(fontType, fontSizeMedium))
                keyLabel.place(rely=0.3, relx=0.35, anchor="e")

                keys = tk.Entry(canvas, font=(fontType, fontSizeMedium), justify="center")

                keysText = "Exemple : clé1, clé2 etc..."

                keys.insert(0, keysText)
                keys.bind("<FocusIn>",
                          lambda args: keys.delete(0, "end") if keys.get() == keysText else print(""))
                keys.bind("<FocusOut>",
                          lambda args: keys.insert(0, keysText) if keys.get() == "" else print(""))

                keys.place(relx=0.5, rely=0.3, anchor="center")

                actionsLabel = tk.Label(canvas, bg=mainColor, text="Action :", font=(fontType, fontSizeMedium))
                actionsLabel.place(rely=0.4, relx=0.35, anchor="e")

                actions = tk.ttk.Combobox(canvas, values=["Supprimer", "Ajouter"],
                                          font=(fontType, fontSizeMedium), justify="center")
                actions.place(relx=0.5, rely=0.4, anchor="center")

                def interpret():
                    action: str
                    if actions.get() == "Ajouter":
                        action = 'add'
                    elif actions.get() == "Supprimer":
                        action = "remove"
                    else:
                        print("Be sure to chose an action!")
                        return
                    loadedStor.userInterpretKey(keys.get() + "&" + action)
                    updateKeyView()

                execute = tk.Button(canvas, text="Exécuter", font=(fontType, fontSizeMedium), command=interpret,
                                    bg=secondColor)
                execute.place(rely=0.5, relx=0.5, anchor="center")

                updateKeyView()

            # ======================================================================================================

            def changeOpenEditMenu(name: str):
                global openEditMenu

                match name:
                    case "editValues":
                        openEditMenu = EditMenus.EDITVALUES
                        matchEditMenu(EditMenus.EDITVALUES)
                    case "editKeys":
                        openEditMenu = EditMenus.EDITKEYS
                        matchEditMenu(EditMenus.EDITKEYS)

            editMenuFrame = tk.Label(canvas, bd=5, relief="groove", name="editMenuBar")

            editValues = tk.Button(editMenuFrame, font=(fontType, fontSizeMedium), bg=secondColor,
                                   text="Modifier Valeurs", name="editValues",
                                   command=lambda: changeOpenEditMenu("editValues"))
            editKeys = tk.Button(editMenuFrame, font=(fontType, fontSizeMedium), bg=secondColor,
                                 text="Modifier Clés", name="editKeys", command=lambda: changeOpenEditMenu("editKeys"))

            fitAllChilds(editMenuFrame)

            editMenuFrame.place(relwidth=1 - 4 / wWidth, relheight=0.05, relx=2 / wWidth)

            def matchEditMenu(openEditMenu):

                match (openEditMenu):

                    case EditMenus.EDITVALUES:
                        editValuesMenu()
                    case EditMenus.EDITKEYS:
                        editKeysMenu()

            matchEditMenu(openEditMenu)

        case Menus.CONTENT:

            highlightButton(menuFrame, "contentMenu")

            clearComponents(canvas)

            content = tk.Text(canvas, font=(fontType, fontSizeBig), bg=mainColor)
            content.insert("end", loadedStor.displayData())
            content.configure(state="disabled")
            content.place(relwidth=1 - 4 / wWidth, relx=2 / wWidth, relheight=0.9)

        case "_":
            raise Exception("Menu Not Found")

    # ======================================================================================================


def main():
    global root, canvas, nextButton

    # define the root of the gui
    root = tk.Tk()
    root.title(f"Character Generator by VoidScientist - v{version}")
    root.geometry(f"{wWidth}x{wHeight}")
    root.resizable(width=False, height=False)

    # main canvas
    canvas = tk.Canvas(root, height=wHeight, width=wWidth, bg=mainColor)
    canvas.place(relheight=1, relwidth=1, rely=0.1)

    nextButton = tk.PhotoImage(file='ressources\\next_button.png')

    # creating components of the GUI
    menuBar()
    changeMenu(openMenu)

    # show the gui
    root.mainloop()


main()
