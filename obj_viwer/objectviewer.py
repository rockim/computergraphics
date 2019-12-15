import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import ctypes
newobj = 0
wfnum = 0
gVertexArraySeparate = None
v = []
vn = []
f = []
gCamAng = 0
gCamHeight = .1
mouse_x = 1
mouse_y = 1
orbit = 0
panning = 0
camera_x = 0
camera_y = 0
panning_zoom = 1
camera_zoom = 1
minus_zoom = 0
angle_v = 0
angle_h = 0
width = 640
height = 640
def render():
    global gVertexArraySeparate
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    gluPerspective(45,1,1,10) #원근법
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)
    
    glTranslatef(camera_x,camera_y,0) # camera translate
    
    glRotated(angle_v, 1,0,0) # camera orbit
    glRotated(angle_h, 0,1,0)
    if camera_zoom >= 0: # zoom in and out
        glScalef(camera_zoom,camera_zoom,camera_zoom)
    else: # except minus of zoom
        glScalef(minus_zoom,minus_zoom,minus_zoom)
    
    drawFrame()
    drawFlat()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_RESCALE_NORMAL)
    
    glPushMatrix()
    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION,lightPos)
    glPopMatrix()
    # light intensity for each color channel
    lightColor = (1.,0.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    # material reflectance for each color channel
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    glPushMatrix()
    if wfnum%2 == 1: #wireframe
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    if gVertexArraySeparate is not None:
        objects_drawarrays()
    glPopMatrix()
    glDisable(GL_LIGHTING)
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0,0,255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
def drawCube():
    glBegin(GL_QUADS)
    glColor3ub(255,255,255)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)

    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)

    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)

    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()
def drawFlat():
    glBegin(GL_LINES)
    glColor3ub(0,255,0)
    for i in range(9):
        if i == 4:
            glColor3ub(255,0,0)
        else:
            glColor3ub(170,170,170)
        glVertex3fv(np.array([-4.,0.,4-i]))
        glVertex3fv(np.array([4.,0.,4-i]))
    for j in range(9):
        if j == 4:
            glColor3ub(0,0,255)
        else:
            glColor3ub(170,170,170)
        glVertex3fv(np.array([4-j,0.,-4.]))
        glVertex3fv(np.array([4-j,0.,4.]))
    glEnd()

def drawSphere(numLats=30, numLongs=30):
    for i in range(0, numLats+1):
        lat0 = np.pi * (-0.5 + float(float(i-1)/float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(float(i)/float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)

        glBegin(GL_TRIANGLE_STRIP)

        for j in range(0 , numLongs +1):
            lng = 2 * np.pi *float(float(j-1)/float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0 ,z0)
            glVertex3f(x * zr1, y * zr1 ,z1)

        glEnd()
def Key_callback(window, key,scancode,action,mods):
    global wfnum
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key==glfw.KEY_Z:
            wfnum += 1
def cursor_callback(window, xpos, ypos):
    global angle_v, angle_h, mouse_x, mouse_y, camera_x, camera_y, camera_zoom, orbit, panning
    if orbit==1:
        if angle_v >= 360:
            angle_v = 0
        elif angle_v <= -360:
            angle_v = 0
        if angle_h >= 360:
            angle_h = 0
        elif angle_h <= -360:
            angle_h = 0
        angle_v += (ypos - mouse_y)*0.3
        angle_h += (xpos - mouse_x)*0.3
        mouse_x = xpos
        mouse_y = ypos
    if panning == 1:
        camera_x += (xpos- mouse_x)/(width/2)
        camera_y -= (ypos- mouse_y)/(height/2)
        mouse_x = xpos
        mouse_y = ypos
def button_callback(window, button, action, mod):
   global mouse_x, mouse_y, orbit, panning
   if button==glfw.MOUSE_BUTTON_LEFT:
       if action==glfw.PRESS:
           (mouse_x, mouse_y) = glfw.get_cursor_pos(window)
           orbit = 1
       elif action==glfw.RELEASE:
           orbit = 0
   if button==glfw.MOUSE_BUTTON_RIGHT:
       if action==glfw.PRESS:
           (mouse_x, mouse_y) = glfw.get_cursor_pos(window)
           panning = 1
       elif action==glfw.RELEASE:
           panning = 0

def scroll_callback(window, xoffset, yoffset):
    global camera_zoom
    if yoffset <0:
        camera_zoom += 0.01
    elif yoffset >0:
        camera_zoom -= 0.01
def drop_callback(window, paths):
    global v, vn, f, gVertexArraySeparate, newobj
    file_name = paths[0].split("/")
    print("File name: ",file_name[-1])
    if newobj == 1:
        v = []
        vn = []
        f = []
    objects = open(paths[0]).read()
    newobj=1
    lineas = objects.splitlines()
    for linea in lineas:
        elem = linea.split()
        if elem:
            if elem[0] == 'v':
                vs = (float(elem[1]), float(elem[2]), float(elem[3]))
                v.append(vs)
            elif elem[0] == 'vn':
                vns = (float(elem[1]), float(elem[2]), float(elem[3]))
                vn.append(vns)
            elif elem[0] == 'f':
                fs = (elem[1].split("/"), elem[2].split("/"), elem[3].split("/"))
                f.append(fs)

    face3 = 0
    face4 = 0
    facehigh = 0
    same_norm = []
    for i in range(0,len(f)):
        same_norm.append((f[i][0][2],f[i][1][2],f[i][2][2]))
    for i in range(0,len(f)):
        same_ver = 0
        for j in range(0, len(f)):
            if same_norm[i] == same_norm[j] and i != j:
                same_ver += 1
        if same_ver == 0:
            face3 += 1
        elif same_ver == 1:
            face4 += 1
        else:
            facehigh += 1

    print("Total number of faces: ", len(f))
    print("Number of faces with 3 vertices: ", face3)
    print("Number of faces with 4 vertices: ", face4)
    print("Number of faces with more than 4 vertices: ", facehigh)
    gVertexArraySeparate = createVertexArraySeparate()

def createVertexArraySeparate():
    global v, vn, f
    if newobj == 0:
        return None
    narr = []
    for facei in range(0,len(f)):
        veci = 0
        posnormi = 0
        while veci is not 3:
            vnnum = int(f[facei][veci][posnormi+2])
            vnum = int(f[facei][veci][posnormi])
            narr.append(vn[vnnum-1])
            narr.append(v[vnum-1])
            veci += 1
    
    varr = np.array(narr,'float32')
    return varr
            
def objects_drawarrays():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3,GL_FLOAT,6*varr.itemsize,ctypes.c_void_p(varr.ctypes.data+3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES,0,int(varr.size/6))
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)


def main():
    global gVertexArraySeparate
    if not glfw.init():
        return
    
    window = glfw.create_window(width,height,"2015004393",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window,Key_callback)
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)


    glfw.terminate()

if __name__=="__main__":
    main()
