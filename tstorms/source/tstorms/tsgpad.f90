  MODULE TSGPAD_MOD
  implicit none
  contains

!######################################################################

  SUBROUTINE GPAD2( Gxx, xx )
  implicit none
  real, intent(in),  dimension(:,:) :: Gxx
  real, intent(out), dimension(:,:) :: xx
  integer :: ix, jx, i, j
  integer :: nx, nx2, nxp1

  ix = SIZE( Gxx, 1 )
  jx = SIZE( Gxx, 2 )

  nx2  = SIZE( xx, 1 ) - SIZE( Gxx, 1 )
  nx   = nx2 / 2
  nxp1 = nx + 1

  xx(nxp1:ix+nx,nxp1:jx+nx) = Gxx(:,:) 

  do i = 1,nx
    xx(i,   nxp1:jx+nx) = xx(ix+i,nxp1:jx+nx)
    xx(i+ix+nx,nxp1:jx+nx) = xx(nx+i,nxp1:jx+nx)
  end do

  do j = 1,nx
    xx(1:ix+nx2,j   ) = xx(1:ix+nx2, nxp1)
    xx(1:ix+nx2,j+jx) = xx(1:ix+nx2,jx)
  end do

  end SUBROUTINE GPAD2

!######################################################################

  SUBROUTINE GPAD1( Gxx, xx )
  implicit none
  real,    intent(in),  dimension(:) :: Gxx
  real,    intent(out), dimension(:) :: xx
  integer :: i, ix, ip 
  integer :: nx, nx2, nxp1
  real    :: dx

  nx2  = SIZE( xx ) - SIZE( Gxx )
  nx   = nx2 / 2
  nxp1 = nx + 1

  ix = SIZE( Gxx )
  ip = SIZE(  xx ) + 1

  xx(nxp1:ix+nx) = Gxx(:) 

  dx = xx(nx+2) - xx(nx+1)

  do i = 1,nx
     xx(   i) =  xx(   nxp1) - ( nxp1 - i ) * dx
     xx(ip-i) =  xx(ip-nxp1) + ( nxp1 - i ) * dx 
  end do

  end SUBROUTINE GPAD1

!######################################################################
  end MODULE TSGPAD_MOD
