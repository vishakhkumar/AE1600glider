//for Canard of Aircraft
canardWingSpan = 3;
canardWingTipChord = 1;
canardWingRootChord = 1.5;
canardWingSweepAngle = 20;
canardWingDihedralAngle = 0;
canardWingXPos = 7;
canardWingAngleOfAttack = 5;

//for Main wing of aircraft
mainWingSpan = 8;
mainWingTipChord = 1;
mainWingRootChord = 2;
mainWingSweepAngle = 10;
mainWingDihedralAngle = 0;
mainWingXPos = -3;  //Yes, yes, I know it's negative, big fucking brohaha.
mainWingAngleOfAttack = 5;

// for fuselage of Aircraft
fuselageLength = 18;
fuselageWidth = 0.25;


module generateWing(Span,TipChord,RootChord,SweepAngle,DihedralAngle,flip)
{

   linear_extrude(height = 1/16, center = true, convexity = 10, twist = 0)
    translate([0, 0, 0])
    if (flip==true)
    {polygon(points=[[0,0],
                    [0+Span,0-Span/tan(90-SweepAngle)],
                    [0+Span,0-Span/tan(90-SweepAngle)-TipChord],
                    [0,0-RootChord],
                    ],
                paths=[[0,1,2,3]]);
    }
    else {    polygon(points=[[0,0],
                    [0-Span,0-Span/tan(90-SweepAngle)],
                    [0-Span,0-Span/tan(90-SweepAngle)-TipChord],
                    [0,0-RootChord],
                    ],
                paths=[[0,1,2,3]]);
    }
//forwardLeft = [0,0,0] //starts from the origin //forwardRight = [0+Span,0-Span/tan(SweepAngle),0]
//backwardLeft = [0,0-RootChord,0] //backwardRight = [0+Span,0-Span/tan(SweepAngle)-TipChord,0]
    }

// actual code begins here

union(){
//drawing the fuselage
cube(size = [fuselageLength,fuselageWidth,fuselageWidth], center = true);
//drawing the wings
translate([mainWingXPos,0,0]){
rotate([mainWingAngleOfAttack,0,90]){
generateWing(Span=mainWingSpan,TipChord=mainWingTipChord,RootChord=mainWingRootChord,SweepAngle=mainWingSweepAngle,DihedralAngle=mainWingDihedralAngle,flip = false);
generateWing(Span=mainWingSpan,TipChord=mainWingTipChord,RootChord=mainWingRootChord,SweepAngle=mainWingSweepAngle,DihedralAngle=mainWingDihedralAngle,flip = true);
};
};

translate([canardWingXPos,0,0]){
rotate([canardWingAngleOfAttack,0,90]){
generateWing(Span=canardWingSpan,TipChord=canardWingTipChord,RootChord=canardWingRootChord,SweepAngle=canardWingSweepAngle,DihedralAngle=canardWingDihedralAngle,flip = true);
generateWing(Span=canardWingSpan,TipChord=canardWingTipChord,RootChord=canardWingRootChord,SweepAngle=canardWingSweepAngle,DihedralAngle=canardWingDihedralAngle,flip = false);
};
};
};
