MODULE ZTOOLS_MOD
implicit none

real, allocatable, dimension(:) :: dx
real                            :: dy

contains

!################################################################

subroutine to_mass_grid( xi, xo )

real, intent(in),  dimension(:,:) :: xi
real, intent(out), dimension(:,:) :: xo

integer :: ixi, jxi, ixo, jxo

ixi = SIZE( xi, 1 )
jxi = SIZE( xi, 2 )
ixo = SIZE( xo, 1 )
jxo = SIZE( xo, 2 )

if( ixi == (ixo+1) ) then
  xo(:,:) =  0.5*( xi(1:ixi-1,:) + xi(2:ixi,:) )
else if( jxi == (jxo+1) ) then
  xo(:,:) =  0.5*( xi(:,1:jxi-1) + xi(:,2:jxi) )
else
  print *, ' *** ERROR IN TRANSFORMATION TO MASS GRID'
  STOP
endif

end subroutine to_mass_grid

!################################################################

subroutine set_dx_dy( rlat, rlon )

real, intent(in),  dimension(:) :: rlat, rlon

 real, parameter :: radius = 6371.0e3 
 real            :: PI, RADIAN
 real            :: dlat, dlon
 integer         :: j
 integer         :: jmx

 jmx = size(rlat)

ALLOCATE( dx(jmx) )

PI     = 4.0*ATAN(1.0)
RADIAN = 180.0/PI

dlat = ABS( rlat(2) - rlat(1) ) / RADIAN
dlon =    ( rlon(2) - rlon(1) ) / RADIAN

do j = 1,jmx
  dx(j) = radius * cos( rlat(j) / RADIAN ) * dlon
end do
  dy    = radius * dlat

end subroutine set_dx_dy

!################################################################

subroutine comp_vort( uu, vv, vort )

real, intent(in),  dimension(:,:) :: uu, vv
real, intent(out), dimension(:,:) :: vort
integer                           :: i,   j
integer                           :: imx, jmx

imx = SIZE( uu, 1 )
jmx = SIZE( uu, 2 )

vort(:,:) = 0.0

do j = 2,jmx-1
do i = 2,imx-1
!vort(i,j) = ( vv(i+1,j) - vv(i-1,j) ) / ( 2.0*dx(j) ) &
!          - ( uu(i,j+1) - uu(i,j-1) ) / ( 2.0*dy    )
vort(i,j) = ( vv(i+1,j) - vv(i-1,j) ) / ( 2.0*dx(j) ) &
          - ( uu(i,j+1) - uu(i,j-1) ) / ( 2.0*dy )
end do
end do

end subroutine comp_vort

!################################################################

subroutine comp_wind( uu, vv, wind )

real, intent(in),  dimension(:,:) :: uu, vv
real, intent(out), dimension(:,:) :: wind

wind(:,:) = uu(:,:)*uu(:,:) + vv(:,:)*vv(:,:)
wind(:,:) = SQRT( wind(:,:) )

end subroutine comp_wind

!################################################################

subroutine comp_psl( psfc, tsfc, zsfc, psl )

 real, parameter :: rgas   = 0.2870e3
 real, parameter :: grav   = 9.806
 real, parameter :: grexp  = grav / rgas

real, intent(in),  dimension(:,:) :: psfc, tsfc, zsfc
real, intent(out), dimension(:,:) :: psl

 psl(:,:) = psfc(:,:) * exp( grexp * zsfc(:,:) / tsfc(:,:) )

end subroutine comp_psl

!################################################################
end MODULE ZTOOLS_MOD
