# MINER

from tkinter import*
import random
import tkinter.messagebox


class Igra():
    """Razred kjer se ustvari polje za igranje igre Miner"""
    def __init__(self, okno):
        #Glavni menu
        glavniMenu = Menu(okno)
        okno.config(menu=glavniMenu) #doda glavni menu v okno
        #Podmenuji
        menuNovaIgra = Menu(glavniMenu,tearoff=0)
        menuTezavnost = Menu(glavniMenu,tearoff=0)
        # Funkcionalnost
        glavniMenu.add_cascade(label='Igra', menu=menuNovaIgra)
        glavniMenu.add_cascade(label='Težavnost', menu=menuTezavnost)
        # Funkcije posameznih 'gumbov'
        menuNovaIgra.add_command(label='Nova Igra', command=self.novaIgra)
        menuNovaIgra.add_command(label='Izhod', command=okno.destroy)

        menuTezavnost.add_command(label='Lahka',command=self.lahko)
        menuTezavnost.add_command(label='Srednja',command=self.srednje)
        menuTezavnost.add_command(label='Težka',command=self.tezko)

        #sličice
        self.slikaM = PhotoImage(file = "mini-mine.gif")
        self.slikaZ = PhotoImage(file = "zastava.gif")
        self.slikaV = PhotoImage(file = "vprasaj.gif")
        
        #Postavitev okna za igranje
        self.frame = Frame(okno)
        self.frame.pack()        

        #zagon igre - privzeta je srednja težavnost
        self.srednje()

        # Ustvarijo se gumbi na (self.n)x(self.n) polju, matrika objektov(gumbov) in
        # matrika Sosedov('Mina' oz. št.sosednjih min ) - self.mine naključno postavljenih min
    def novaIgra(self):
        '''Ustvari polje gumbov, matriko gumbov(objektov) in matriko sosedov, ki za vsak gumb pove ali
        je tam mina ali pa število min okoli gumba'''
        #self.koliko šteje koliko gumbov smo že pritisnili, da vemo, kdaj ostanejo samo še mine
        self.koliko = 0 
        mesta = random.sample(range(self.n*self.n), self.mine)
        self.matrikaGumbov = []
        k = 0
        #v seznamu sezSosedov bo niz 'Mina' oz. število min okoli posameznega elementa
        sezSosedov = [0]*(self.n*self.n)
        for vrstica in range(self.n):
            elementiGumbov = []
            for stolpec in range(self.n):
                self.gumb = Button(self.frame, width=2, bg='grey', command=self.kateri(vrstica,stolpec))
                self.gumb.bind("<Button-3>", self.zastava(vrstica,stolpec))
                self.gumb.grid(row=vrstica, column=stolpec)
                if k in mesta:
                    seznam = [k-1,k+1,k-(self.n-1),k-self.n,k-(self.n+1),k+(self.n-1),k+(self.n),k+(self.n+1)]
                    sezSosedov[k] = 'Mina'
                #če je k element, ki bi se moral nahajati na levem ali desnem robu matrike(polja), ne smemo 
                #upostevati levih oz desnih sosedov, ker bi v seznamu na tak način upoštevali napačne elemente 
                #(bi preskočili na drugi rob polja)
                    if (k+1)%self.n == 0:
                        seznam = [k-1,k-(self.n+1),k-self.n,k+(self.n-1),k+(self.n)]
                    elif k%self.n == 0:
                        seznam = [k+1,k-self.n,k-(self.n-1),k+(self.n),k+(self.n+1)]
                    for sosed in seznam:
                #ker se na zgornjem robu zgodi, da so v seznamu tudi negativni elementi - upoštevamo samo pozitivne
                        if sosed >= 0:
                #varovalna zanka, da ne vrača napake, če je na mestu, kjer bi moral prišteti ena niz 'Mina'
                            try:
                                sezSosedov[sosed] += 1
                            except:
                                pass          
                elementiGumbov.append(self.gumb)
                k += 1
            self.matrikaGumbov.append(elementiGumbov)
        #iz sezSosedov ustvarimo matriko sosedov velikosti (self.n)x(self.n)
        self.matrikaSos = [sezSosedov[i:i+self.n] for i in range(0,len(sezSosedov),self.n)]


    def zastava(self,a,b):
        '''če kliknemo na gumb enkrat z desnim klikom se na gumbu pojavi zastava, če dvakrat pa vprašaj'''
        def pomozna(event):
            if self.matrikaGumbov[a][b]['bg']=='snow4':
                self.matrikaGumbov[a][b].config(bg='snow3',image=self.slikaV)
            elif self.matrikaGumbov[a][b]['bg']=='snow3':
                self.matrikaGumbov[a][b].config(bg='grey',image = '', height=0, width=2, state=NORMAL)
            elif self.matrikaGumbov[a][b]['bg']=='grey':
                self.matrikaGumbov[a][b].config(bg='snow4',image = self.slikaZ, height=20, width=18)
        return pomozna

        
    def odpri(self,a,b):
        '''Funkcija, ki rekurzivno odpre polje, če kliknemo na gumb, ki v okolici nima min'''
        self.matrikaGumbov[a][b].config(bg='rosy brown', state=DISABLED, relief='sunken')
        sez = [(a,b+1),(a,b-1),(a+1,b),(a+1,b+1),(a+1,b-1),(a-1,b),(a-1,b+1),(a-1,b-1)]
        for x,y in sez:
            #v vseh sosednjih poljih pogledamo če je tam število od 1 do 8 (na takšnem gumbu se izpiše število sosednjih min)
            #ali pa 0 - na takšnem gumbu zopet pokličemo funkcijo odpri
            if x in range(self.n) and y in range(self.n) and self.matrikaGumbov[x][y]['bg']=='grey':
                if self.matrikaSos[x][y] in [1,2,3,4,5,6,7,8]:
                    self.koliko +=1
                    self.matrikaGumbov[x][y].config(bg='white',text=str(self.matrikaSos[x][y]),relief='sunken',state=DISABLED)
                if self.matrikaSos[x][y] == 0:
                    self.koliko +=1
                    self.odpri(x,y)
 
    def kateri(self, a,b):
        '''Dobi informacijo na kateri gumb smo kliknili(z levim klikom) in se primerno odzove:
        če je bila tam mina igro izgubimo, če okoli gumba ni nobene mine odpre polje toliko,
        dokler niso na robu samo gumbi, ki imajo v okolici vsaj eno mino oziroma, če je v okolici
        gumba vsaj ena mina pokaže na gumbu število min okoli njega'''    
        def dogodek():
            '''Pomožna funkcija'''
            #prvi if stavek moramo dati zaradi zastavic/vprašajev, ki jih postavljamo, da uporabnik ne more klikniti na tak gumb
            if  self.matrikaGumbov[a][b]['bg'] == 'grey':
                if self.matrikaSos[a][b] == 'Mina':
                    #odpremo vse gumbe z mino in končamo igro
                    for vrstica in range(self.n):
                        for stolpec in range(self.n):
                            if self.matrikaSos[vrstica][stolpec] == 'Mina':
                                self.matrikaGumbov[vrstica][stolpec].config(bg='rosy brown',image = self.slikaM, height=16, width=16)
                    self.matrikaGumbov[a][b].config(bg='red',image = self.slikaM, height=16, width=16)
                    #če kliknemo mino se odpre okno, ki pove, da smo igro izgubili
                    tkinter.messagebox.showinfo("Konec igre", "Konec")
                    odgovor = tkinter.messagebox.askquestion('Nova igra', 'Začnem novo igro?')
                    if odgovor == 'yes':
                        self.novaIgra()
                    else:
                        okno.destroy()
                elif self.matrikaSos[a][b] == 0:
                    self.koliko +=1
                    self.odpri(a,b)
                else:
                    self.koliko +=1
                    self.matrikaGumbov[a][b].config(bg='white', text=str(self.matrikaSos[a][b]),relief='sunken',state=DISABLED)
                #če so ostale neodprte samo še mine zmagamo
                if self.koliko == (self.n*self.n) - self.mine:
                    tkinter.messagebox.showinfo("Zmaga", "Bravo")
                    odgovor1 = tkinter.messagebox.askquestion('Nova igra', 'Začnem novo igro?')
                    if odgovor1 == 'yes':
                        self.novaIgra()
                    else:
                        okno.destroy()
        return dogodek

    #Funkcije za težavnost
    def lahko(self):
        '''Nastavi velikost polja in število min na lahko težavnost'''
        #nastavimo parametre za velikost polja in število min
        self.n = 10
        self.mine = 11
        #zbrišemo prejšnji okvir in ustvarimo novega
        self.frame.destroy()
        okno.geometry("240x260")
        self.frame = Frame(okno)
        self.frame.pack()
        #zagon igre
        self.novaIgra()
        
    def srednje(self):
        '''Nastavi velikost polja in število min na srednjo težavnost'''
        self.n = 20
        self.mine = 63
        self.frame.destroy()
        okno.geometry("480x520")
        self.frame = Frame(okno)
        self.frame.pack()
        self.novaIgra()

    def tezko(self):
        '''Nastavi velikost polja in število min na težko težavnost'''
        self.n = 25
        self.mine = 131
        self.frame.destroy()
        okno.geometry("600x650")
        self.frame = Frame(okno)
        self.frame.pack()
        self.novaIgra()


if __name__ == "__main__":
    #Naredimo glavno okno in nastavimo ime
    okno = Tk()
    okno.title('Miner')
    aplikacija = Igra(okno)
    okno.mainloop()
