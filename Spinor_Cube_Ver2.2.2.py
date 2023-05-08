import numpy as np
import mayavi
from mayavi import mlab

from numpy import arange, pi, cos, sin, exp, sqrt

from traits.api import HasTraits, Range, Instance, \
        on_trait_change
from traitsui.api import View, Item, Group

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, \
                MlabSceneModel

import clifford 
from clifford.g3c import *

R12 = lambda lam : exp(-e12*pi*lam)
R23 = lambda lam : exp(-e23*pi*lam)
R31 = lambda lam : exp(e13*pi*lam)
T = lambda v : 1 - (v ^ einf / 2)
#!!! have to set parenthesis like this, ^ operator follows -


def mlog(M):
    '''
    Motor logarithm from Chasles' Theorem
    as described in
    Dorst 2009, Geometric Algebra for Computer Science (Revised Edition), pp. 283

    M : Motor of form M = T_v R_Btheta
    '''
    R = -eo | (M*einf)
    #print("R",R)
    v = -2 * (eo | M)*R.inv()

    if R == 1.0:
        return -v*einf/2

   # print("v",v)

    B = R(2)/sqrt(float(-R(2)**2))
   # print("B",B)

    theta = -2 * np.arctan2(float(R(2)*B.inv()),float(R(0)))

   # print("theta",theta)

    lg = 1/2 * (-(v^B)*B.inv() + (1-R**2).inv()*((v|B)*theta))*einf - B*theta/2

    return lg

def generate_weights():
        
    B1_ = lambda alpha : (alpha-1)**2
    B2_ = lambda alpha : 10*alpha**2*(alpha-1)**4
    B3_ = lambda alpha : (alpha)**3

    # normalization of weight funtions 
    norm = lambda alpha : B1_(alpha) + B2_(alpha) + B3_(alpha)   
    B1,B2,B3 = lambda alpha : B1_(alpha)/norm(alpha), lambda alpha : B2_(alpha)/norm(alpha), lambda alpha : B3_(alpha)/norm(alpha)

    return B1,B2,B3

def generate_rotors(string_axis,rotation_axis):

    rotation_bivector = - rotation_axis / (e1^e2^e3) #dual plane in Cl(3,0)
    rotation = lambda lam : exp(-rotation_bivector*pi*lam)

    twist_bivector = - string_axis / (e1^e2^e3)
    twist = exp(twist_bivector*pi/2)

    # control point on cube side and halfway in interpolation
    side    = lambda lam : rotation(lam)*0.3*string_axis*~rotation(lam)
    halfway = lambda lam : rotation(lam)*string_axis*~rotation(lam)

    # define roto-translation motors
    M1 = lambda lam : T(side(lam))    * rotation(lam) * twist
    M2 = lambda lam : T(halfway(lam)) * rotation(lam) * twist 
    M3 = lambda lam : T(2.0*string_axis)    
    
    return M1,M2,M3

def interpolate(B1,B2,B3,M1,M2,M3):

    return lambda alpha,lam : exp( B1(alpha)*mlog(M1(lam)) + B2(alpha)*mlog(M2(lam)) + B3(alpha)*mlog(M3(lam)))



class Cubes:
    def __init__(self,elems):
        
        self.elems = elems

    def s(self, Rotor): #Sandwich product

        return Cubes(Rotor*self.elems*~Rotor)

Cube = Cubes(np.array([e1 + e2 + e3, e1 - e2 + e3,
                       -e1 - e2 + e3, -e1 + e2 + e3,
                       e1 + e2 - e3, e1 - e2 - e3,
                       -e1 - e2 - e3, -e1 + e2 - e3,]))

up_ = np.array([
    +e1+e2+e3,
    -e1+e2+e3,
    +e1-e2+e3,
    -e1-e2+e3,
])  
down_ = np.array([
    +e1+e2-e3,
    -e1+e2-e3,
    +e1-e2-e3,
    -e1-e2-e3,
]) 
front = np.array([
    +e1+e2+e3,
    -e1+e2+e3,
    +e1+e2-e3,
    -e1+e2-e3,
]) 
back = np.array([
    +e1-e2+e3,
    -e1-e2+e3,
    +e1-e2-e3,
    -e1-e2-e3,
]) 
left = np.array([
    -e1+e2+e3,
    -e1-e2+e3,
    -e1+e2-e3,
    -e1-e2-e3,
]) 
right = np.array([
    +e1+e2+e3,
    +e1-e2+e3,
    +e1+e2-e3,
    +e1-e2-e3,
]) 

faces = 0.3*np.array([
    right,front, up_,
    left, back,  down_,
])

faces = faces.reshape((6,2,2))
Cube = Cubes(faces)

R = [R23,R31,R12]
def cube_faces(lam):
    
    b = 3 #axis of rot

    RotCube = Cube.s(R[abs(b)-1](lam))
    
    return RotCube.elems

def string_points(lam,string_axis,rotation_axis,cr=None):
    
    B1,B2,B3 = generate_weights()
    M1,M2,M3 = generate_rotors(string_axis,rotation_axis) #string,rot axis

    # interpolation param alpha
    alpha = np.linspace(0,1,30)

    # interpolated rotors M
    M = interpolate(B1,B2,B3,M1,M2,M3)(alpha,lam)

        
    # apply
    c = string_axis / e123 / rotation_axis #for e3 rotation : e1 -> e2, e2 -> e1
    if cr is not None:
        c = R12(-cr/2)*c*~R12(-cr/2) # +1/4 two versions?
        
    right,left = up(0.1*c),up(-0.1*c)
    # ribbon control points
    right_boundary,left_boundary = M*right*~M, M*left*~M
      
    return down(np.array([right_boundary,left_boundary]))


class MyModel(HasTraits):
    lam    = Range(-1.0, 1.0, 0.0)  # mode='spinner')

    scene = Instance(MlabSceneModel, ())
    
    #mult plot instances for mult refeshes?
    face_plot1 = Instance(PipelineBase)
    face_plot2 = Instance(PipelineBase)
    face_plot3 = Instance(PipelineBase)
    face_plot_1 = Instance(PipelineBase)
    face_plot_2 = Instance(PipelineBase)
    face_plot_3 = Instance(PipelineBase)
    
    string_plot_x1 = Instance(PipelineBase)
    string_plot_x2 = Instance(PipelineBase)
    
    string_plot_y1 = Instance(PipelineBase)
    string_plot_y2 = Instance(PipelineBase)
    
    string_plot_z1 = Instance(PipelineBase)
    string_plot_z2 = Instance(PipelineBase)

    
        
    # When the scene is activated, or when the parameters are changed, we
    # update the plot.

    
    @on_trait_change('lam,scene.activated')
    def update_plot(self):
        
        #self.lam = round(self.lam,2)
        
        faces = cube_faces(self.lam)
        ribbon_x1 = string_points(self.lam, e1,e3)
        ribbon_x2 = string_points(self.lam + 1,-e1,e3)
        
        ribbon_y1 = string_points(self.lam + 1.5 ,e2,e3)
        ribbon_y2 = string_points(self.lam + 0.5 ,-e2,e3)
        
        ribbon_z1 = R12(self.lam/2)*string_points(0.5,e3,e2,cr=self.lam)*~R12(self.lam/2)
        ribbon_z2 = R12(self.lam/2)*string_points(1.5,-e3,e2,cr=self.lam)*~R12(self.lam/2)
        
        colors = ((1,0,0),(0,1,0),(0,0,1))
        
        self.face_plot1; self.face_plot2; self.face_plot3
        self.face_plot_1; self.face_plot_2; self.face_plot_3
    
        
        ##### --> iter through self plot attributes 
        face_plots = ["face_plot1","face_plot2","face_plot3",
                      "face_plot_1","face_plot_2","face_plot_3"]
        
        
        for face_plot,face,color in zip(face_plots,faces,2*colors): #gives rotated face elems
            x,y,z = (np.array((face|e1)(0),dtype=float),
                     np.array((face|e2)(0),dtype=float),
                     np.array((face|e3)(0),dtype=float))
                
            if vars(self)[face_plot] is None: # if not initialized
                vars(self)[face_plot] = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = color)
            else: # just updating the plot
                vars(self)[face_plot].mlab_source.trait_set(x=x, y=y, z=z) 
        
        
        ### plotting the ribbon +x (red)
        x,y,z = (np.array((ribbon_x1|e1)(0),dtype=float),
                 np.array((ribbon_x1|e2)(0),dtype=float),
                 np.array((ribbon_x1|e3)(0),dtype=float))
        
        if self.string_plot_x1 is None: # if not initialized
            self.string_plot_x1 = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = (1,0,0), representation = "surface")
        else: # just updating the plot
            self.string_plot_x1.mlab_source.trait_set(x=x, y=y, z=z) 
        
        #'''#####
        ### -x (red)
        
        x,y,z = (np.array((ribbon_x2|e1)(0),dtype=float),
                 np.array((ribbon_x2|e2)(0),dtype=float),
                 np.array((ribbon_x2|e3)(0),dtype=float))
        
        if self.string_plot_x2 is None: # if not initialized
            self.string_plot_x2 = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = (1,0,0), representation = "surface")
        else: # just updating the plot
            self.string_plot_x2.mlab_source.trait_set(x=x, y=y, z=z) 
        
        ### +y (green)
        x,y,z = (np.array((ribbon_y1|e1)(0),dtype=float),
                 np.array((ribbon_y1|e2)(0),dtype=float),
                 np.array((ribbon_y1|e3)(0),dtype=float))
        
        if self.string_plot_y1 is None: # if not initialized
            self.string_plot_y1 = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = (0,1,0), representation = "surface")
        else: # just updating the plot
            self.string_plot_y1.mlab_source.trait_set(x=x, y=y, z=z) 
        
        ### -y (green)
        x,y,z = (np.array((ribbon_y2|e1)(0),dtype=float),
                 np.array((ribbon_y2|e2)(0),dtype=float),
                 np.array((ribbon_y2|e3)(0),dtype=float))
        
        if self.string_plot_y2 is None: # if not initialized
            self.string_plot_y2 = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = (0,1,0), representation = "surface")
        else: # just updating the plot
            self.string_plot_y2.mlab_source.trait_set(x=x, y=y, z=z) 
            
        ### +z (blue)
        x,y,z = (np.array((ribbon_z1|e1)(0),dtype=float),
                 np.array((ribbon_z1|e2)(0),dtype=float),
                 np.array((ribbon_z1|e3)(0),dtype=float))
        
        if self.string_plot_z1 is None: # if not initialized
            self.string_plot_z1 = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = (0,0,1), representation = "surface")
        else: # just updating the plot
            self.string_plot_z1.mlab_source.trait_set(x=x, y=y, z=z) 
        
        ### -z (blue)
        x,y,z = (np.array((ribbon_z2|e1)(0),dtype=float),
                 np.array((ribbon_z2|e2)(0),dtype=float),
                 np.array((ribbon_z2|e3)(0),dtype=float))
        
        if self.string_plot_z2 is None: # if not initialized
            self.string_plot_z2 = self.scene.mlab.mesh(x,y,z,opacity=1.0, color = (0,0,1), representation = "surface")
        else: # just updating the plot
            self.string_plot_z2.mlab_source.trait_set(x=x, y=y, z=z) 
        
        ##### '''
        
    # The layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=500, width=600, show_label=False),
                Group(
                        '_', 'lam',
                     ),
                resizable=True,
                )

my_model = MyModel()
my_model.configure_traits()


