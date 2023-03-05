

/****************************************** */
const{app,BrowserWindow, Menu}=require('electron')
const path = require('path')


const craeteWindow = () => {
    const mainWindow = new BrowserWindow({
       width: 1920,
       height: 1080,
       webPreferences: {
          nodeIntegration: true,
          contextIsolation:false,
          devTools: false
       }
    })
    
    mainWindow.loadFile('./Frontend/intro.html')
    mainWindow.setTitle("OPTIF")
   // mainWindow.setIcon(path.join(__dirname, './src/icon.png'))
    //mainWindow.setMenu(null) // enlever le menu 
    mainWindow.webContents.openDevTools() // open dev tools
    let menu=Menu.buildFromTemplate([
       {
          label:"Quitter",
          submenu:[
             
               
                {label:'Quitter', 
                click(){
                   app.quit()
                }
               }
             
          ]
       }
    ])
    Menu.setApplicationMenu(menu)
 }


 app.whenReady().then(() => {
      craeteWindow()

      app.on('activate', () => {
         if (BrowserWindow.getAllWindows().length === 0) createWindow()
         // si le nombre de windows 0 créer une 
         
      })
   })

