module bearing()
{
    difference()
    {
        rotate([0,90,0]) color("orange") cylinder(h = 19, d=12,  center = true);
        translate([-1,0,0]) rotate([0,90,0]) color("orange") cylinder(h = 22, d=6,  center = true);
    }
}
