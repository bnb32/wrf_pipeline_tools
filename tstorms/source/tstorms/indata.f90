  MODULE INDATA_MOD
!=====================================================================
  use ncfile_mod,        only: NCFILE_TYPE
  use netcdf_file_mod,   only: READ_FILE_HEADER
  use ncread_write_mod,  only: AXIS_VALUES, READ_VARIABLE, TIME_AXIS_VALUES
  use ncfile_access_mod, only: AXIS_LENGTH, VAR_AXIS_LEN
  use get_date_mod,      only: CURRENT_DATE
  use ztools_mod,        only: SET_DX_DY, COMP_VORT, COMP_WIND

  implicit none

  type(NCFILE_TYPE) :: file
  integer           :: imx, jmx, nmx

  real, allocatable, dimension(:) :: time

!=====================================================================
! --- NAMELIST
!=====================================================================

  character*120 :: fname        = '       '
        logical :: do_smoothing = .false.
	logical :: do_thickness = .false.
        logical :: use_sfc_wnd  = .true.
        real    :: atwc         = 0.5
  character(100) :: work_dir
  character(100) :: nml_name = "nml_input"
  character(200) :: nml_full

  namelist / nml_indata / fname, do_smoothing, do_thickness, use_sfc_wnd, atwc

!=====================================================================
  contains

!######################################################################

  SUBROUTINE SET_GRID 
!=====================================================================
! --- READ FILE HEADER, GET DIMENSIONS
!=====================================================================
  implicit none

  CALL GETARG(1,work_dir)
  nml_full = TRIM(work_dir) // "/" // TRIM(nml_name)
  nml_full = TRIM(nml_full)
  OPEN( UNIT = 101, FILE = nml_full )
  READ( 101, nml_indata )
  CLOSE( 101 )

  file = READ_FILE_HEADER( TRIM( fname ) )

  nmx = AXIS_LENGTH( file, 'time'  )
  imx = AXIS_LENGTH( file, 'lon'   )
  jmx = AXIS_LENGTH( file, 'lat'   )

  !WRITE(*,*) '        ' 
  !WRITE(*,*) TRIM( fname  ) 
  !WRITE(*,*) '        ' 
  !WRITE(*,*) ' imx, jmx, nmx = ', imx, jmx, nmx
  !WRITE(*,*) '        ' 

!=====================================================================
  end SUBROUTINE SET_GRID

!######################################################################

  SUBROUTINE SET_LOLA( rlon, rlat )
!=====================================================================
! --- SET LONGITUDE & LATITUDE ETC 
!=====================================================================
  implicit none

  real, intent(out), dimension(:) :: rlon, rlat
 
  integer :: k

!=====================================================================

  
  CALL AXIS_VALUES( file, 'lon', rlon )

  CALL AXIS_VALUES( file, 'lat', rlat )

  CALL SET_DX_DY( rlat, rlon )

!--------------------------------------------------------

!    print *, '  '
!    print *, ' longitudes'
!  do k = 1,imx
!    print *, k, rlon(k)
!  end do
!    print *, '  '
!    print *, ' latitudes'
!  do k = 1,jmx
!    print *, k, rlat(k)
!  end do

!--------------------------------------------------------

  ALLOCATE( time(nmx) )

  CALL TIME_AXIS_VALUES( file, time )

!=====================================================================
  end SUBROUTINE SET_LOLA

!######################################################################

  SUBROUTINE GET_DATA( itime, wind,  vor, tbar,  psl, thick, &
                       year,  month, day, hour )
!=====================================================================
  implicit none

  integer, intent(in)                  :: itime
  real,    intent(out), dimension(:,:) :: wind, vor, tbar, psl, thick
  integer, intent(out)                 :: year, month, day, hour

  integer, dimension(3) :: start
  integer, dimension(6) :: date

  real, dimension(size(wind,1),size(wind,2)) :: wrk1, wrk2

  real :: rtime, rmax, rmin

!=====================================================================

  start(1) = 1        !--- x dimension
  start(2) = 1        !--- y dimension
  start(3) = itime    !--- t dimension
  rtime    = time(itime)

  CALL CURRENT_DATE( file, rtime, date )

  !print *, date

  year  = date(1)
  month = date(2)
  day   = date(3)
  hour  = date(4)

!-------------------------------------------------------------------
! --- U & V at 850 mb
!-------------------------------------------------------------------
  
  CALL READ_VARIABLE( file, 'U850', start, wrk1 )
     rmax = maxval( wrk1(:,:) )!,mask=wrk1.lt.1.0E20 )
     rmin = minval( wrk1(:,:) )
     !print *, ' **** uu: ', rmax, rmin

  CALL READ_VARIABLE( file, 'V850', start, wrk2 )
     rmax = maxval(  wrk2(:,:) )!,mask=wrk2.lt.1.0E20 )
     rmin = minval(  wrk2(:,:) )
     !print *, ' **** vv: ', rmax, rmin

!-------------------------------------------------------------------
! --- Vorticity at 850 mb
!-------------------------------------------------------------------

  CALL COMP_VORT( wrk1, wrk2, vor )
     rmax = maxval(  vor(:,:) )
     rmin = minval(  vor(:,:) )
     !print *, ' **** vor: ', rmax, rmin

!-------------------------------------------------------------------
! --- Wind Speed at 850 mb or lowest model level
!-------------------------------------------------------------------

  if( use_sfc_wnd ) then
     !print *, ' *** using wind speed at models lowest level' 

     CALL READ_VARIABLE( file, 'UBOT', start, wrk1 )
       rmax = maxval(  wrk1(:,:) )
       rmin = minval(  wrk1(:,:) )
       !print *, ' **** uu: ', rmax, rmin

     CALL READ_VARIABLE( file, 'VBOT', start, wrk2 )
       rmax = maxval(  wrk2(:,:) )
       rmin = minval(  wrk2(:,:) )
       !print *, ' **** vv: ', rmax, rmin
  else
     !print *, ' *** using wind speed at 850 mb'
  endif

  CALL COMP_WIND( wrk1, wrk2, wind )
     rmax = maxval(  wind(:,:) )!,mask=wind.lt.1.0E20 )
     rmin = minval(  wind(:,:) )
     !print *, ' **** wind: ', rmax, rmin

!-------------------------------------------------------------------
! --- Temperature for warm core layer
!-------------------------------------------------------------------

     CALL READ_VARIABLE( file, 'T200', start, wrk1 )
     CALL READ_VARIABLE( file, 'T500', start, wrk2 ) 

     tbar(:,:) = atwc * wrk1(:,:) + (1.0-atwc) * wrk2(:,:)

     rmax = maxval(  tbar(:,:) )
     rmin = minval(  tbar(:,:) )
     !print *, ' **** tbar: ', rmax, rmin

!-------------------------------------------------------------------
! --- Sea level pressure
!-------------------------------------------------------------------

  CALL READ_VARIABLE( file, 'PSL', start, psl )

     rmax = maxval(  psl(:,:) )
     rmin = minval(  psl(:,:) )
     !print *, ' **** psl: ', rmax, rmin

!-------------------------------------------------------------------
! --- Thickness between 1000 and 200 mb
!-------------------------------------------------------------------

  !if ( do_thickness ) then
  
    CALL READ_VARIABLE( file, 'Z200',  start, wrk1 )
    CALL READ_VARIABLE( file, 'Z1000', start, wrk2 ) 

     thick(:,:) = wrk1(:,:) - wrk2(:,:)

     rmax = maxval(  thick(:,:) )
     rmin = minval(  thick(:,:) )
     !print *, ' **** thick: ', rmax, rmin

  !endif

!-------------------------------------------------------------------
! --- OPTIONAL SMOOTHING
!-------------------------------------------------------------------
  if( do_smoothing ) then

    CALL AVG9( psl, wrk1 )
    CALL AVG9( vor, wrk1 )

     !print *, '   AFTER SMOOTHING:'
     rmax = maxval(  vor(:,:) )
     rmin = minval(  vor(:,:) )
     !print *, ' **** vor: ', rmax, rmin
     rmax = maxval(  psl(:,:) )
     rmin = minval(  psl(:,:) )
     !print *, ' **** psl: ', rmax, rmin

  endif

!=====================================================================
  end SUBROUTINE GET_DATA

!######################################################################

  subroutine avg9( xx, wrk )
  implicit none
  real, intent(inout), dimension(:,:) :: xx, wrk
  integer                             :: i, j

  wrk(:,:) = xx(:,:)

  do j = 2,jmx-1
  do i = 2,imx-1
     xx(i,j) = SUM( wrk(i-1:i+1,j-1:j+1) ) / 9.0
  end do
  end do

  end subroutine avg9

!######################################################################
  end MODULE INDATA_MOD
